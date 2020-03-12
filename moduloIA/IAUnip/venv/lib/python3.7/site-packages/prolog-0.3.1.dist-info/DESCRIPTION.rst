======
prolog
======

Tools and convenience methods to simplify and expedite Python logging.

* Simple - though opinionated - setup for common use-cases
* Extensively and easily configurable via user and local files, as well as environ variables
* Comes with full featured formatters and handlers that can also be used
  in normal ``logging`` situations

Usage
=====

``basic_config``
----------------

The easiest way to begin using ``prolog`` is to add the following to your
application code::

    import prolog
    prolog.basic_config()

This will configure the ``root`` logger for the default level ``logging.INFO``
and set up two handlers: a colorized, console streaming handler, as well as a file
handler set to log to the default file - ``pypro.log`` - in the main app's directory.

To specify select loggers defined in application or library code, you pass the
comma-seperated names of the desired loggers::

    prolog.basic_config('myapp,another_app')

``basic_config`` accepts the following parameters:


``loggers``
    The desired loggers to configure; can be either a comma-separated
    string of logger names, a list of ``Logger`` instances, or ``None``
    for the root logger.

``level``
    Specify the logging level for all loggers and handlers. Can be
    either the numeric value or string name for the desired level.

``handlers``
    The handlers to add to the given ``loggers``; can be a comma-separated
    string of shortcut names ('stream' or 'file', by default) or a list
    of ``Handler`` instances.

``propagate``
    Indicates whether each ``logger`` instance will be set to propagte.

``reset_handlers``
    If True, force a reset of all currently configured handlers.

``cfg``
    The ``prolog.config.PrologConfig`` instance to use. If not given,
    the default will be used (``prolog.config.config``). For all
    preceding parameters except for ``loggers`` set to None (the default),
    ``cfg`` will be used to determine the appropriate setting.



Examples
--------

Once installed, **prolog** can be invoked to show configuration settings or
sample usage::

    $ python -m prolog sample --level=DEBUG basic

.. image:: https://raw.githubusercontent.com/dakrauth/prolog/master/resources/basic-output.png

Setting colors via environments variables::

    $ export PYPROLOG_LEVEL_COLORS='CRITICAL:white,red;ERROR:lightred;DEBUG:lightgray,cyan;*:gray,gray'
    $ python -m prolog sample --level=DEBUG basic

.. image:: https://raw.githubusercontent.com/dakrauth/prolog/master/resources/env-color-output.png

Develop and testing
===================

::

    $ pip install invoke
    $ inv develop
    $ inv test

Configuration
=============

Prolog can be configured via a number of different options:

* User-level configuration file, using ``appdirs`` to determine the user's
  configuration directory plus ``pyprolog/config``, which must be a JSON encoded
  file containing a dictionary overriding any of the defaults listed below
* Current working directory configuration file ``.pyprologrc``, also JSON
* Environment variables, see below
* Manipulation of the default ``prolog.config.config`` instance or instantiating
  your own
* Generating a ``logging.config.dictConfig`` dict via ``prolog.config.dict_config``

Defaults
--------

::

    LEVEL = 'INFO'
    SHORT_FMT = "{levelname}:{name} {message}"
    LONG_FMT = '[{asctime} {name}:{levelname}:{module}:{lineno}] {message}'

    COLOR_LONG_FMT = '{color}[{asctime} {name}:{levelname}:{module}:{lineno}]{endcolor} {message}'
    COLOR_SHORT_FMT = '{color}{levelname}:{name}{endcolor} {message}'
    LEVEL_COLORS = 'DEBUG:magenta;INFO:blue;WARNING:yellow;ERROR:red;CRITICAL:white,red'

    DATE_FMT = "%Y-%m-%dT%H:%M:%S"
    STYLE_FMT = '{'

    HANDLERS = 'stream,file'
    PROPAGATE = False
    DISABLE_EXISTING = True
    RESET_HANDLERS = True

    STREAM_LEVEL = 'NOTSET'
    STREAM_FORMATTER = 'color'
    STREAM_STREAM = 'sys.stderr'

    FILE_LEVEL = 'NOTSET'
    FILE_FORMATTER = 'long'
    FILE_FILENAME = 'pypro.log'
    FILE_MAX_BYTES = 0
    FILE_BACKUP_COUNT = 0

Environment
-----------

By default, the ``prolog.config.config`` instance will load any environment
variable begging with ``PYPROLOG_`` and ending with any of the defaults listed
above. For instance, to override the default logging level, do the following
before executing your application code::

    $ export PYPROLOG_LEVEL='DEBUG'
    $ python myapp.py



