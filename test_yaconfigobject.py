# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('.'))

import logging
logging.basicConfig(level=logging.DEBUG)

from yaconfigobject import Config

TEST_CONFIG1 = """
configitem:
    subitem1: 1
    subitem2: 2
    subitem3: 3
"""

TEST_CONFIG2 = """
configitem:
    subitem2: 4
    
another:
    item: string
"""


def test_package_base():
    """Test if the calling module basepath trickery is doing its thing."""

    config = Config()

    assert config._package_base == os.path.abspath('.')


def test_load(tmpdir):
    """Test if we can load a config file."""
    configfolder = tmpdir.mkdir('config')
    configfile1 = configfolder.join('config.yaml')
    configfile1.write(TEST_CONFIG1)

    config = Config(paths=[str(configfolder)], name='config.yaml')

    assert len(config.configitem) == 3
    assert config.configitem.subitem1 == 1
    assert config.configitem.subitem2 == 2
    assert config.configitem.subitem3 == 3

    # Also check if default config name works

    config = Config(paths=[str(configfolder)])

    assert len(config.configitem) == 3
    assert config.configitem.subitem1 == 1
    assert config.configitem.subitem2 == 2
    assert config.configitem.subitem3 == 3


def test_update(tmpdir):
    """Test if updating works."""
    config_folder1 = tmpdir.mkdir('config1')
    configfile1 = config_folder1.join('config.yaml')
    configfile1.write(TEST_CONFIG1)
    config_folder2 = tmpdir.mkdir('config2')
    configfile2 = config_folder2.join('config.yaml')
    configfile2.write(TEST_CONFIG2)

    config1 = Config(paths=[str(config_folder1)], name='config.yaml')

    assert config1.configitem.subitem2 == 2

    config2 = Config(paths=[str(config_folder2)], name='config.yaml')

    assert config2.configitem.subitem2 == 4

    config1.update(config2)

    assert config1.configitem.subitem2 == 4
    assert config1.configitem.subitem1 == 1
    assert config1.configitem.subitem3 == 3


def test_kwargs():

    TEST_STRING = 'a test string'

    config = Config(testitem=TEST_STRING)

    assert config.testitem == TEST_STRING
