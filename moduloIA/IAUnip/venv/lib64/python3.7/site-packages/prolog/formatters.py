import sys
import logging
from textwrap import indent
from .config import config

__all__ = ['PrologFormatter', 'ColorFormatter', 'Colorize']


class PrologFormatter(logging.Formatter):
    DEFAULT_FMT = config.LONG_FMT
    DEFAULT_DATEFMT = config.DATE_FMT
    DEFAULT_STYLE = config.STYLE_FMT

    def __init__(self, fmt=None, datefmt=None, style=None):
        super().__init__(
            fmt=fmt or self.DEFAULT_FMT,
            datefmt=datefmt or self.DEFAULT_DATEFMT,
            style=style or self.DEFAULT_STYLE
        )

    @staticmethod
    def to_str(value):
        '''
        Convert value a string. If value is already a str or None, returne it
        unchanged. If value is a byte, decode it as utf8. Otherwise, fall back
        to the value's repr.
        '''
        if value is None:
            return ''

        if isinstance(value, str):
            return value
        
        elif isinstance(value, bytes):
            return value.decode()

        return repr(value)

    def formatException(self, ei):
        return indent(super().formatException(ei), '... ')

    def formatMessage(self, record):
        try:
            record.msg = self.to_str(record.msg)
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        return super().formatMessage(record)
        #return formatted.replace("\n", "\n    ")


class Colorize:
    fg = {
        'gray':      '0;30', 'black':        '1;30', 'darkgray':    '0;30',
        'red':       '0;31', 'lightred':     '1;31', 'darkred':     '0;31',
        'green':     '0;32', 'lightgreen':   '1;32', 'darkgreen':   '0;32',
        'brown':     '0;33', 'lightbrown':   '1;33', 'darkbrown':   '0;33', 
        'blue':      '0;34', 'lightblue':    '1;34', 'darkblue':    '0;34',
        'magenta':   '0;35', 'lightmagenta': '1;35', 'darkmagenta': '0;35',
        'purple':    '0;35', 'lightpurple':  '1;35', 'darkpurple':  '0;35',
        'cyan':      '0;36', 'lightcyan':    '1;36', 'darkcyan':    '0;36',
        'lightgray': '0;37', 'white':        '1;37', 'yellow':      '1;33',
    }
    bg = {
        'black': '40', 'red':    '41', 'green':   '42',
        'brown': '43', 'blue':   '44', 'magenta': '45',
        'cyan':  '46', 'purple': '45', 'gray':    '47',
    }
    reset = '\x1b[0m'

    @classmethod
    def style(cls, fg='', bg=''):
        code_list = []
        if fg:
            code_list.append(cls.fg[fg])
        
        if bg:
            code_list.append(cls.bg[bg])

        return '\x1b[{}m'.format(';'.join(code_list)) if code_list else ''

    @staticmethod
    def supported(stream=sys.stderr):
        return hasattr(stream, 'isatty') and stream.isatty()


class ColorFormatter(PrologFormatter):
    DEFAULT_FMT = config.COLOR_LONG_FMT
    DEFAULT_COLORS = config.LEVEL_COLORS

    def __init__(self, fmt=None, datefmt=None, style=None, colors=None):
        super().__init__(fmt, datefmt, style)
        if Colorize.supported():
            self.colors = self.normalize_colors(colors or self.DEFAULT_COLORS)
        else:
            self.colors = {}
            
    @staticmethod
    def normalize_colors(colors):
        if isinstance(colors, str):
            colors = dict(
                bits.split(':') for bits in colors.split(';') if bits
            )

        colors = {key: val.split(',') for key, val in colors.items()}
        default = colors.pop('*', False)
        if default:
            for level in logging._nameToLevel:
                if level not in colors:
                    colors[level] = default

        return colors

    def set_colors(self, record):
        if record.levelname in self.colors:
            record.color = Colorize.style(*self.colors[record.levelname])
            record.endcolor = Colorize.reset
        else:
            record.color = record.endcolor = ''

    def formatMessage(self, record):
        self.set_colors(record)
        return super().formatMessage(record)


registered_formatters = {
    'long': PrologFormatter(),
    'short': PrologFormatter(fmt=config.SHORT_FMT, datefmt=None),
    'color': ColorFormatter(),
}
registered_formatters['default'] = registered_formatters['long']


def get_formatter(arg=None):
    if arg is None:
        return registered_formatters['default']
    elif isinstance(arg, logging.Formatter):
        return arg
    elif isinstance(arg, str):
        try:
            return registered_formatters[arg]
        except KeyError as e:
            msg = '"{}" unrecognized formatter shortcut'.format(arg)
            raise KeyError(msg) from e
    elif isinstance(arg, dict):
        return PrologFormatter(**arg)
    else:
        return PrologFormatter(*arg)

