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

logger = logging.getLogger(__name__)

CONFIGNAME = 'config.yaml'

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass


class ConfigContainer(dict):
    """A dictionary object holding all config items.
    """

    def load(self, conffile):
        """Load an arbitrary configuration file. Multiple files can be loaded,
        the last file loaded will take precedence over previously loaded files.
        """
        logger.info('Loading configuration file: {}'.format(conffile))

        with open(conffile) as f:
            self.update(yaml.load(f))

    def __setattr__(self, key, val):
        self.__setitem__(key, val)

    def __getattr__(self, key):
        return self.__getitem__(key)

    def update(self, other):
        """Modify update function for consistent handling of nested
        ConfigContainers.
        """
        for key, val in other.items():
            if isinstance(val, dict):
                if key in self:
                    self[key].update(ConfigContainer(val))
                else:
                    self.__setitem__(key, ConfigContainer(**val))
            else:
                self.__setitem__(key, val)


class Config(ConfigContainer):
    def __init__(self, paths=None, name=None, **kwargs):

        if name is None:
            name = CONFIGNAME

        if paths is None:
            logger.debug('No config paths specified! Trying to guess some...')

            calling_frame = inspect.getframeinfo(
                inspect.stack()[0].frame.f_back)
            logger.debug('{}'.format(
                inspect.getframeinfo(inspect.stack()[0].frame.f_back)))
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
            logger.debug('Trying to load {}.'.format(filepath))

            if os.path.exists(filepath):
                logger.info('Loading {}.'.format(filepath))
                self.load(filepath)

                nconfig += 1

        if nconfig == 0:
            logger.critical('!!! No configuration file loaded !!!')

        super(Config, self).__init__(**kwargs)
