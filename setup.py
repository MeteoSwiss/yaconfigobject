#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020, MeteoSwiss, the authors

from setuptools import setup


setup(name='yaconfigobject',
      use_scm_version=True,
      author='Philipp Falke',
      author_email='philipp.falke@meteoswiss.ch',
      description='A library representing YAML config files as object.',
      entry_points={},
      py_modules=['yaconfigobject'],
      include_package_data=True,
      package_data={'': ['README.md'],
                    },
      license='MIT License',
      long_description=open('README.md').read(),
      setup_requires=['setuptools_scm'],
      install_requires=[
          'pyyaml',
      ]
      )
