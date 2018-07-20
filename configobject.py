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


__all__ = ['Config',
           'ConfigContainer',
           'CONFIG',
           ]


import os
import yaml
import logging

import inspect


CONFIGNAME = 'config.yaml'


class ConfigContainer(dict):
    """A dictionary object holding all config items.
    """

    def load(self, conffile):
        """Load an arbitrary configuration file. Multiple files can be loaded,
        the last file loaded will take precedence over previously loaded files.
        """
        logging.info('Loading configuration file: {}'.format(conffile))

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


class Config(object):

    def __init__(self, paths=None, name=None, calling_frame=None):

        self.config = ConfigContainer()

        if name is None:
            name = CONFIGNAME

        if paths is None:
            logging.debug('No config paths specified! Trying to guess some...')

            if calling_frame is None:
                calling_frame = inspect.stack()[0].frame.f_back
            calling_basefolder = os.path.dirname(calling_frame.filename)
            calling_package = os.path.basename(calling_basefolder)
            paths = [os.getcwd(),
                     os.path.abspath(
                         os.path.expanduser(
                             '~/.config/{}'.format(calling_package))),
                     '{}/config'.format(calling_basefolder),
                     ]

        nconfig = 0
        for path in paths[::-1]:
            filepath = os.path.join(path, name)
            logging.debug('Trying to load {}.'.format(filepath))

            if os.path.exists(filepath):
                logging.info('Loading {}.'.format(filepath))
                self.config.load(filepath)

                nconfig += 1

        if nconfig == 0:
            logging.critical('!!! No configuration file loaded !!!')

    def __call__(self):
        return self.config


def _get_CONFIG_calling_frame(stack):
    for frame in stack:
        if frame.code_context is not None and \
                'from configobject import CONFIG\n' in frame.code_context:
            return frame
    return None


CONFIG = Config(paths=None, name=None,
                calling_frame=_get_CONFIG_calling_frame(inspect.stack()))()
