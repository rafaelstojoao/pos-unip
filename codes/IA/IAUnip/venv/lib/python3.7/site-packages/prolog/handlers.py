import logging
import logging.handlers
from .config import config
from . import formatters

__all__ = [
    'create_handler',
    'stream_handler',
    'file_handler',
    'get_handlers',
    'reset_handlers',
    'PrologStreamHandler',
    'PrologFileHandler',
]

class PrologMixin:
    
    def setFormatter(self, formatter):
        formatter = formatters.get_formatter(formatter)
        super().setFormatter(formatter)


class PrologStreamHandler(PrologMixin, logging.StreamHandler):
    
    def __init__(self, stream=None, **kwargs):
        if isinstance(stream, str):
            stream = config.string_import(stream)

        super().__init__(stream=stream, **kwargs)


class PrologFileHandler(PrologMixin, logging.handlers.RotatingFileHandler):
    pass


def create_handler(cls, level=config.LEVEL, formatter='default', **kwargs):
    formatter = formatters.get_formatter(formatter)
    h = cls(**kwargs)
    h.setFormatter(formatter)
    h.setLevel(level)
    return h


def stream_handler(
    level=config.STREAM_LEVEL,
    formatter=config.STREAM_FORMATTER,
    stream=config.STREAM_STREAM
):
    return create_handler(PrologStreamHandler, level, formatter, stream=stream)


def file_handler(
    level=config.FILE_LEVEL,
    formatter=config.FILE_FORMATTER,
    filename=config.FILE_FILENAME,
    maxBytes=config.FILE_MAX_BYTES,
    backupCount=config.FILE_BACKUP_COUNT
):
    return create_handler(
        PrologFileHandler,
        level,
        formatter,
        filename=filename,
        maxBytes=maxBytes,
        backupCount=backupCount
    )


registered_handlers = {
    'stream': stream_handler,
    'file': file_handler
}


def reset_handlers():
    logging._handlers.clear()
    del logging._handlerList[:]


def extract_items(names):
    if isinstance(names, str):
        names = names.split(',')
    elif not isinstance(names, (list, tuple)):
        names = [names]

    for name in names:
        if isinstance(name, str):
            for subname in name.split(','):
                yield subname
        else:
            yield name


def get_handlers(names, level, reset=True):
    handlers = []
    if reset:
        reset_handlers()

    for item in extract_items(names):
        if isinstance(item, logging.Handler):
            handler = item

        elif isinstance(item, str):
            try:
                handler = registered_handlers[item]
            except KeyError as e:
                msg = '"{}" unrecognized handler shortcut'.format(item)
                raise KeyError(msg) from e

            if not isinstance(handler, logging.Handler):
                handler = handler(level)
                registered_handlers[item] = handler

        elif issubclass(item, logging.Handler):
            raise ValueError('Cannot instantiate from ...Handler class ')

        else:
            handler = item(level)

        handlers.append(handler)

    return handlers
