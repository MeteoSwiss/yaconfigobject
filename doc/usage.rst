=====
Usage
=====

Set up your yaml configuration file (e.g. *package_name.conf*) and define a CONFIG instance in your package::

    from yaconfigobject import Config
    CONFIG = Config(name='package_name.conf')


Access the attributes::

    CONFIG.main


The installation path is always available::

    CONFIG._package_base


All environment variables prefixed with your package name will be considered a
config value. Use uppercase letters and **_** instead of **.**::

    import os
    os.environ['DEMO_MAIN_APP'] = "Demo app with configuration"

    from package_name import CONFIG
    CONFIG.main.app

