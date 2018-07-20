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

    def __init__(self, paths=None, name=None):

        self.config = ConfigContainer()

        if paths is None:
            logging.debug('No config paths specified! Trying to guess some...')
            calling_module = inspect.getmodule(inspect.stack()[0].frame.f_back)
            calling_package = calling_module.__package__
            paths = [os.getcwd(),
                     os.path.abspath(
                         os.path.expanduser(
                             '~/.configi/{}'.format(calling_package))),
                     '{}/static'.format(
                         os.path.dirname(calling_module.__file__)),
                     ]

        for path in paths[::-1]:
            logging.debug('Trying to load {}.'.format(path))
            filepath = os.path.join(path, name)
            if os.path.exists(filepath):
                logging.info('Loading {}.'.format(filepath))
                self.config.load(filepath)

    def __call__(self):
        return self.config


CONFIG = Config(paths=None, name=None)()
