yaconfigobject
==============

Yet Anoter Configuration Object, this time using YAML.

A Python package that provides application wide configuration as an object,
where all configuration items are accessible as attributes directly:

```python
from yaconfigobject import Config

property = Config.topic.subtopic
```

Configurations are stored in a YAML file inside the `module/static` directory
of the application. A file called `config.yaml` exists in the applications
current working directory will take precedence over the packaged file (in the
`static` directory).
