import logging
from .formatters import *
from .handlers import *
from .config import *

def basic_config(
    loggers=None,
    level=None,
    handlers=None,
    propagate=None,
    reset_handlers=None,
    cfg=None
):
    '''
    Configure and initialize loggers and handlers, based on the following
    options::

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
    '''
    cfg = cfg or config
    level = cfg.resolve('LEVEL', level, 'INFO')
    logging._acquireLock()
    try:
        handlers = get_handlers(
            cfg.resolve('HANDLERS', handlers),
            level,
            cfg.resolve('RESET_HANDLERS', reset_handlers)
        )
        for name in config.logger_names(loggers):
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.propagate = cfg.resolve('PROPAGATE', propagate)
            for h in handlers:
                logger.addHandler(h)
    finally:
        logging._releaseLock()
