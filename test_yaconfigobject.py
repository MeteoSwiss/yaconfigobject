# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath('.'))

import logging
logging.basicConfig(level=logging.DEBUG)

import pytest

from yaconfigobject import Config, ConfigError

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

    config3 = Config(paths=[str(config_folder1)], name='config.yaml')
    config4 = Config(paths=[str(config_folder2)], name='config.yaml')

    config5 = config3 + config4
    assert config5.configitem.subitem2 == 4
    assert config5.configitem.subitem1 == 1
    assert config5.configitem.subitem3 == 3


def test_kwargs():

    TEST_STRING = 'a test string'

    config = Config(testitem=TEST_STRING)

    assert config.testitem == TEST_STRING


def test_check_folders(tmpdir):
    folder1 = tmpdir.mkdir('exists')
    configfile = folder1.join('config.yaml')
    configfile.write(TEST_CONFIG1)

    config = Config(paths=[str(folder1)], name='config.yaml')
    config['existing_folder'] = str(folder1)

    assert config.check_folders() == []

    config['non_existing_dir'] = os.path.join(str(tmpdir), 'does_not_exist')

    with pytest.raises(ConfigError):
        config.check_folders(keyword='dir')

    config['new_folder'] = os.path.join(str(tmpdir), 'will_be_created')

    with pytest.raises(ConfigError):
        config.check_folders(keyword='folder', create=False)

    assert [os.path.join(str(tmpdir), 'will_be_created')] == \
        config.check_folders(create=True)
