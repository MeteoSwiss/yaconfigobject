yaconfigobject Documentation
==============================

Yet Anoter Configuration Object, this time using YAML.

A Python package that provides application wide configuration as an object,
where all configuration items are accessible as attributes directly::

    from yaconfigobject import Config
    CONFIG = Config()
    property = CONFIG.topic.subtopic

Configurations are stored in a YAML file inside the ``module/config`` directory
of the application. A file called ``config.yaml`` existing in the applications
current working directory will take precedence over the packaged file (in the
``config`` directory).


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   usage
   yaconfigobject
   contributing
   authors
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
