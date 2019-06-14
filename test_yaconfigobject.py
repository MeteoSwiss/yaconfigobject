# -*- coding: utf-8 -*-

import os

import logging

import pytest

from yaconfigobject import Config, ConfigError, ConfigContainer

logging.basicConfig(level=logging.DEBUG)

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


def test_env_variable_config(tmpdir):
    test_app_name = 'myapp'
    configfolder = tmpdir.mkdir('config')
    configfile1 = configfolder.join('{}.yaml'.format(test_app_name))
    configfile1.write(TEST_CONFIG1)

    os.environ['_'.join([test_app_name.upper(), 'CONFIGITEM',
                         'SUBITEM1'])] = '10'
    os.environ['_'.join([test_app_name.upper(), 'CONFIGITEM',
                         'SUBITEM2'])] = '20'
    os.environ['_'.join([test_app_name.upper(), 'CONFIGITEM',
                         'SUBITEM4'])] = 'four'

    config = Config(
        paths=[str(configfolder)], name='{}.yaml'.format(test_app_name))

    assert config.configitem.subitem1 == 10
    assert config.configitem.subitem2 == 20
    assert config.configitem.subitem3 == 3
    assert config.configitem.subitem4 == 'four'

    test_app_name2 = 'my_amazing_app'
    configfolder2 = tmpdir.mkdir('config2')
    configfile2 = configfolder2.join('{}.yaml'.format(test_app_name2))
    configfile2.write(TEST_CONFIG1)

    os.environ['_'.join([test_app_name2.upper(), 'CONFIGITEM',
                         'SUBITEM1'])] = '11'
    os.environ['_'.join([
        test_app_name2.upper(), 'CONFIGITEM', 'CONTAINS', 'MANY', 'NESTED',
        'SUBITEMS'
    ])] = '12'

    config2 = Config(
        paths=[str(configfolder2)], name='{}.yaml'.format(test_app_name2))
    assert config2.configitem.subitem1 == 11

    assert isinstance(config2.configitem.contains.many.nested, ConfigContainer)
    assert config2.configitem.contains.many.nested.subitems == 12


def test_env_variable_clashes(tmpdir):
    test_app_name = 'another_app'
    configfolder = tmpdir.mkdir('config3')
    configfile = configfolder.join('{}.yaml'.format(test_app_name))
    configfile.write(TEST_CONFIG1)

    os.environ['_'.join([test_app_name.upper(),
                         'ERROR_ITEM_ONE'])] = 'the_real_thing'
    os.environ['_'.join([test_app_name.upper(),
                         'ERROR_ITEM_ONE_SUBITEM'])] = 'not_set'

    config = Config(
        paths=[str(configfolder)], name='{}.yaml'.format(test_app_name))

    # intended behaviour: the highest hierarchy value takes precedence
    assert config.error.item.one == 'the_real_thing'

    with pytest.raises(AttributeError):
        config.error.item.one.subitem
