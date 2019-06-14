#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, MeteoSwiss,
# Author: Philipp Meier <philipp.meier@meteoswiss.ch>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = [
    'Config',
    'ConfigContainer',
]

import os
import yaml
import logging

import inspect

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    pass

logger = logging.getLogger(__name__)

CONFIGNAME = 'config.yaml'


class ConfigError(Exception):
    pass


class ConfigContainer(dict):
    """A dictionary object holding all config items.
    """

    def load(self, conffile):
        """Load an arbitrary configuration file. Multiple files can be loaded,
        the last file loaded will take precedence over previously loaded files.
        """
        logger.info('Loading configuration file: %s', conffile)

        with open(conffile) as f:
            self.update(yaml.load(f, Loader=yaml.SafeLoader))

    def __setattr__(self, key, val):
        self.__setitem__(key, val)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __add__(self, other):
        self.update(other)
        return self

    def update(self, other):
        """Modify update function for consistent handling of nested
        ConfigContainers.
        """
        for key, val in other.items():
            if isinstance(val, dict):
                if key not in self:
                    self[key] = ConfigContainer()
                try:
                    self[key].update(ConfigContainer(val))
                except AttributeError:
                    pass

            else:
                self.__setitem__(key, val)

    def check_folders(self, keyword='folder', create=False):
        """Perform check if folders exist. Folders are identified by a keyword
        as a substring of the corresponding field name.

        Kwargs:
            keyword (str): Keyword identifying folder fields in the config
                file. All fields containing this keyword as a substring are
                considered.
            create (boolean): Whether non-existing folders will be created or
                not.

        Returns:

        """
        created_folders = []

        for key, val in self.items():
            if isinstance(val, ConfigContainer):
                val.check_folders(keyword=keyword, create=create)
            else:
                if keyword in key:
                    self[key] = os.path.abspath(
                        os.path.expanduser(os.path.expandvars(val)))
                    logger.debug('Checking presence of %s', self[key])
                    if not os.path.isdir(self[key]):
                        if create:
                            logger.info('Creating folder %s', self[key])
                            os.makedirs(self[key])
                            created_folders.append(self[key])
                        else:
                            raise ConfigError('Folder %s does not exist!',
                                              self[key])
        return created_folders


class Config(ConfigContainer):
    def __init__(self, paths=None, name=None, **kwargs):

        if name is None:
            name = CONFIGNAME

        if paths is None:
            logger.debug('No config paths specified! Trying to guess some...')

            calling_frame = inspect.getframeinfo(
                inspect.stack()[0].frame.f_back)
            logger.debug('%s',
                         inspect.getframeinfo(inspect.stack()[0].frame.f_back))
            self._package_base = os.path.dirname(calling_frame.filename)
            calling_package = os.path.basename(self._package_base)
            paths = [
                os.getcwd(),
                os.path.abspath(
                    os.path.expanduser(
                        os.path.join('~', '.config',
                                     '{}').format(calling_package))),
                os.path.join('{}', 'config').format(self._package_base),
            ]

        nconfig = 0
        for path in paths[::-1]:
            filepath = os.path.join(path, name)
            logger.debug('Trying to load %s.', filepath)

            if os.path.exists(filepath):
                logger.info('Loading %s.', filepath)
                self.load(filepath)

                nconfig += 1

        if nconfig == 0:
            logger.critical('!!! No configuration file loaded !!!')

        self.from_environment(name)

        super(Config, self).__init__(**kwargs)

    def from_environment(self, name):
        """Update config values based on environment variables prefixed with
        an uppercase `conffile` base name (iwthout extension).

        Args:
            name (str): Full path to the config file

        Returns:
            (dict): A dictionary containing all config values found within
                    environment variables.

        """

        env_var_prefix = os.path.splitext(os.path.basename(name))[0].upper()
        if '_' in env_var_prefix:
            token_start_idx = env_var_prefix.count('_') + 1
        else:
            token_start_idx = 1

        env_config = {}
        for env_var, value in os.environ.items():
            if env_var.startswith(env_var_prefix):
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                config_tokens = env_var.split('_')[token_start_idx:]
                self.update(dict_from_tokens(config_tokens, value))


def dict_from_tokens(tokens, value):
    """Build a dict-tree from a list of tokens defining a unique branch within
    the tree.

    Args:
        tokens (list): A list of tokens defining a branch within the nested dict
        value (any): An object set as the leaf of a branch

    Returns:
        dict: A nested dictionary

    """

    if len(tokens) == 0:
        return value

    key = tokens.pop(0).lower()
    return {key: dict_from_tokens(tokens, value)}
