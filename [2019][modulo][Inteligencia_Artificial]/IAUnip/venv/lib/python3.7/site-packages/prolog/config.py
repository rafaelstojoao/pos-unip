import os
import json
from appdirs import user_config_dir
__all__ = ['BaseConfig', 'PrologConfig', 'dict_config', 'config']

path = os.path

CONSTANTS = {'TRUE': True, 'FALSE': False, 'NONE': None}

def absolute_path(pth):
    return path.normpath(path.expandvars(path.expanduser(pth)))


def data_dict(obj):
    return {k: getattr(obj, k) for k in dir(obj) if k.isupper() and k[0] != '_'}


class BaseConfig:

    def __init__(
        self,
        app_name,
        env_prefix=None,
        local_cfg_filename=None,
        load_env=True,
        load_user=True,
        load_local=True
    ):
        self.env_prefix = env_prefix or (app_name.upper() + '_')

        local_cfg_filename = local_cfg_filename or '.{}rc'.format(app_name)
        self.local_cfg_filename = absolute_path(local_cfg_filename)
        
        fn = os.environ.get('{}_CONFIG'.format(self.env_prefix), None)
        self.user_cfg_filename = absolute_path(fn) if fn else path.join(
            user_config_dir(app_name),
            'config.json'
        )

        data = self.load(load_user, load_local, load_env)
        self.update(**data)

    def load(self, load_user=True, load_local=True, load_env=True):
        data = {}
        if load_user:
            data.update(self.load_user_cfg())

        if load_local:
            data.update(self.load_local_cfg())

        if load_env:
            data.update(self.load_env())
        
        return data

    def load_env(self):
        data = {}
        n = len(self.env_prefix)
        for key, value in (
            (k[n:], v)
            for k,v in os.environ.items()
            if k.startswith(self.env_prefix)
        ):
            key = key.upper()
            if hasattr(self, key):
                data[key] = CONSTANTS.get(value.upper(), value)
        return data

    def load_cfg(self, filename):
        fpath = absolute_path(filename)
        if path.exists(fpath):
            with open(fpath) as fp:
                text = fp.read()
            try:
                return json.loads(text)
            except json.JSONDecodeError as why:
                import warnings
                msg = 'Unable to parse file {}: {}'.format(fpath, str(why))
                warnings.warn(msg)
        return {}

    def load_user_cfg(self):
        return self.load_cfg(self.user_cfg_filename)

    def load_local_cfg(self):
        return self.load_cfg(self.local_cfg_filename)

    def save_cfg(self, filename):
        dirname = path.dirname(filename)
        if dirname and not path.exists(dirname):
            os.makedirs(dirname)

        with open(filename, 'w') as fp:
            json.dump(self.data(), fp, indent='    ')

    def save_user_cfg(self):
        self.save_cfg(self.user_cfg_filename)

    def save_local_cfg(self):
        self.save_cfg(self.local_cfg_filename)

    def remove_cfg(self):
        if path.exists(self.user_cfg_filename):
            os.remove(self.user_cfg_filename)

    def reset(self):
        for key in self.default_data().keys():
            self.__dict__.pop(key, None)

    def data(self):
        return data_dict(self)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    def logger_names(self, names=None):
        if not names:
            names = [None]
        elif isinstance(names, str):
            names = names.split(',')

        return names

    def resolve(self, label, value, default=None):
        return getattr(self, label, default) if value is None else value

    @classmethod
    def default_data(cls):
        return data_dict(cls)

    @staticmethod
    def string_import(dotted_path):
        try:
            mod_path, attr = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImportError('{} not a dotted path string'.format(dotted_path))

        mod = __import__(mod_path)

        try:
            return getattr(mod, attr)
        except AttributeError:
            raise ImportError('Module "{}" has no "{}" attribute'.format(
                mod_path, attr
            ))


class PrologConfig(BaseConfig):
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


config = PrologConfig('pyprolog')


def dict_config(
    loggers=None,
    level=None,
    propagate=None,
    disable_existing=None,
    cfg=None
):
    '''
    Generate a configuration dict to use with ``logging.config.dictConfig``
    '''
    cfg = cfg or config
    level = cfg.resolve('LEVEL', level, 'INFO')
    propagate = cfg.resolve('PROPAGATE', propagate)
    dct = {
        'version': 1,
        'disable_existing_loggers': cfg.resolve('DISABLE_EXISTING', disable_existing),
        'formatters': {
            'long': {
                '()': 'prolog.formatters.PrologFormatter',
                'format': cfg.LONG_FMT,
                'datefmt': cfg.DATE_FMT,
                'style': cfg.STYLE_FMT
            },
            'short': {
                '()': 'prolog.formatters.PrologFormatter',
                'format': cfg.SHORT_FMT,
                'datefmt': '',
                'style': cfg.STYLE_FMT
            },
            'color': {
                '()': 'prolog.formatters.ColorFormatter',
                'format': cfg.COLOR_LONG_FMT,
                'datefmt': cfg.DATE_FMT,
                'style': cfg.STYLE_FMT,
                'colors': cfg.LEVEL_COLORS
            }
        },
        'handlers': {
            'stream': {
                'class': 'prolog.handlers.PrologStreamHandler',
                'level': cfg.STREAM_LEVEL,
                'formatter': 'color',
            },
            'file': {
                'class': 'prolog.handlers.PrologFileHandler',
                'level': cfg.FILE_LEVEL,
                'formatter': 'long',
                'filename': cfg.FILE_FILENAME,
                'maxBytes': cfg.FILE_MAX_BYTES,
                'backupCount': cfg.FILE_BACKUP_COUNT
            }
        },
        'loggers': {}
    }

    handlers = cfg.HANDLERS.split(',')
    for name in cfg.logger_names(loggers):
        cfg = {'handlers': handlers, 'level': level, 'propagate': propagate}
        if name:
            dct['loggers'][name] = cfg
        else:
            dct['root'] = cfg

    return dct


