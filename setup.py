#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018, MeteoSwiss, Philipp Meier <philipp.meier@meteoswiss.ch>

from setuptools import setup
import versioneer


setup(name='configobject',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Philipp Meier',
      author_email='philipp.meier@meteoswiss.ch',
      description='A library for providing YAML config files as object.',
      entry_points={},
      py_modules=['configobject'],
      include_package_data=True,
      package_data={'': 'README.md',
                    },
      license='MIT License',
      long_description=open('README.md').read(),
      install_requires=[
          'pyyaml',
      ]
      )
