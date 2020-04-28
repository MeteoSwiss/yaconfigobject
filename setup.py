#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020, MeteoSwiss, the authors

from setuptools import setup

requirements = [
    'pyyaml',
]

setup_requirements = [
    'setuptools_scm',
]

test_requirements = [
    'pytest',
]

extras = {
    'test': test_requirements,
}

packages = {}

package_dir = {}

package_data = {}

setup(name='yaconfigobject',
      use_scm_version=True,
      author='Philipp Falke',
      author_email='philipp.falke@meteoswiss.ch',
      description='A library representing YAML config files as object.',
      long_description=open('README.md').read() + '\n\n' +
                     open('HISTORY.rst').read(),
      long_description_content_type="text/markdown",
      url='https://github.com/MeteoSwiss/yaconfigobject',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
      ],
      license='BSD-3-Clause license',
      keywords='yaconfigobject',
      entry_points={},
      py_modules=['yaconfigobject'],
      include_package_data=True,
      install_requires = requirements,
      package_dir = package_dir,
      package_data = package_data,
      setup_requires = setup_requirements,
      tests_require = test_requirements,
      extras_require = extras,
      )
