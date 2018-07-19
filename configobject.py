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


__all__ = ['CONFIG',
           ]


import os
import yaml
import logging


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


CONFIGNAME = 'config.yaml'
CONFIGFILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static',
                                          CONFIGNAME))

LOCALCONFIG = os.path.join(os.getcwd(), CONFIGNAME)


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


CONFIG = ConfigContainer()
CONFIG.load(CONFIGFILE)
if os.path.isfile(LOCALCONFIG):
    CONFIG.load(LOCALCONFIG)
