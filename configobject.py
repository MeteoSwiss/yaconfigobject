#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
