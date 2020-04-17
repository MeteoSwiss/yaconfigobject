=====
Usage
=====

Use in a module
---------------

To make sure every piece of code has access to the same configured information,
it is recommended to instantiate a ``Config`` object in the modules ``__init__.py``
file. The ``Config`` object needs to be present before any other imports take
place.

An example ``__init__.py``::

    from yaconfigobject import Config
    CONFIG = Config('module.yaml')

    from .module_main import *


Advanced usage
--------------

Several options might help you adapting the ``Config`` class to your needs.

Defining search paths
^^^^^^^^^^^^^^^^^^^^^^

To tell ``yaconfigobject.Config()`` where to search for config files, the
``paths`` keyword argument can be specified as a list::

    CONFIG = Config(paths=['~', '~/.local/share/my_app'])

Using custom config file names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For applications where different parts use a separate configuration, it is
highly recommended to use a custom file name::

    CONFIG = Config(name='my_app.yaml')

Adding values in code
^^^^^^^^^^^^^^^^^^^^^

Of course you can also specify config values through code::

    from yaconfigobject import Config

    static_config = Config(database='sqlite:///:memory:')

    CONFIG = Config(name='my_app.yaml')
    CONFIG.update(static_config)

Loading config values from environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``yaconfigobject`` will try to load config values from environment variables
prefixed with the uppercase module or application name when initialising a
``Config`` object::

    CONFIG = Config(name='my_app.yaml')

All environment variables starting with ``MY_APP`` will be considered a config
value. Config items from the environment will always take precedence.

> **NOTE:** When using environment variables, config item identifiers cannot
> contain underscores(``_``)! The app / module name is the only exception.
