#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018, MeteoSwiss, Philipp Meier <philipp.meier@meteoswiss.ch>

from setuptools import setup
import versioneer


setup(name='yaconfigobject',
      use_scm_version=True,
      author='Philipp Meier',
      author_email='philipp.meier@meteoswiss.ch',
      description='A library representing YAML config files as object.',
      entry_points={},
      py_modules=['yaconfigobject'],
      include_package_data=True,
      package_data={'': 'README.md',
                    },
      license='MIT License',
      long_description=open('README.md').read(),
      setup_requires=['setuptools_scm'],
      install_requires=[
          'pyyaml',
      ]
      )
