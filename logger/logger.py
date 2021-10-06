import logging

from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'INFO': GREEN,
    'DEBUG': WHITE,
    'WARNING': YELLOW,
    'ERROR': RED,
    'CRITICAL': YELLOW,
}

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

LOGFILE = 'service_template.log'
LOG_DIR = (Path(__file__).parent / 'log_files')


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class FileExcInfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return True


class StreamExcInfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.exc_info = None
        record.exc_text = ''
        return True


def create_logger(name=__name__) -> logging.Logger:
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()

    new_log = logging.getLogger(name)
    new_log.setLevel(logging.DEBUG)

    stream_h = logging.StreamHandler()
    file_h = TimedRotatingFileHandler(LOG_DIR / LOGFILE,
                                      when='midnight',
                                      interval=1,
                                      backupCount=14,
                                      encoding="UTF-8")
    file_h.suffix = "%Y-%m-%d.log"

    file_h.addFilter(FileExcInfoFilter())
    stream_h.addFilter(StreamExcInfoFilter())

    # Set level
    stream_h.setLevel(logging.DEBUG)
    file_h.setLevel(logging.DEBUG)

    # Set stream formatter:
    stream_text_format = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    stream_color_format = formatter_message(stream_text_format, True)
    stream_formatter = ColoredFormatter(stream_color_format)
    stream_h.setFormatter(stream_formatter)

    # Set file formatter:
    file_formatter = logging.Formatter(u'%(levelname)-9s [%(asctime)s] %(message)s (%(filename)s:%(lineno)d)')
    file_h.setFormatter(file_formatter)

    # Add handlers
    new_log.addHandler(file_h)
    new_log.addHandler(stream_h)

    return new_log


log = create_logger()
