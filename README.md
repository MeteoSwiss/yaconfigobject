yaconfigobject
==============

Yet Anoter Configuration Object, this time using YAML.

A Python package that provides application wide configuration as an object,
where all configuration items are accessible as attributes directly:

```python
from yaconfigobject import Config

CONFIG = Config()

property = CONFIG.topic.subtopic
```

Configurations are stored in a YAML file inside the `module/config` directory
of the application. A file called `config.yaml` existing in the applications
current working directory will take precedence over the packaged file (in the
`config` directory).


Use in a module
---------------

To make sure every piece of code has access to the same configured information,
it is recommended to instantiate a `Config` object in the modules `__init__.py`
file. The `Config` object needs to be present before any other imports take
place.

An example `__init__.py`:

```python
from yaconfigobject import Config

CONFIG = Config('module.yaml')

from .module_main import *
```


Advanced usage
--------------

Several options might help you adapting the ``Config`` class to your needs.

### Defining search paths

To tell ``yaconfigobject.Config()`` where to search for config files, the
``paths`` keyword argument can be specified as a list:

```python
CONFIG = Config(paths=['~', '~/.local/share/my_app'])
```

### Using custom config file names

For applications where different parts use a separate configuration, it is 
highly recommended to use a custom file name:

```python
CONFIG = Config(name='my_app.yaml')
```

### Adding values in code

Of course you can also specify config values through code:

```python
from yaconfigobject import Config

static_config = Config(database='sqlite:///:memory:')

CONFIG = Config(name='my_app.yaml')
CONFIG.update(static_config)
```
