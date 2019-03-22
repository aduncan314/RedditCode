import logging
import os
import functools

from datetime import datetime as dt


def initialize_logging():
    filename = _get_filename()
    level = _get_log_level()
    fmt_string = '[%(asctime)s,%(msecs)03d][%(levelname)s]\t%(module)25s\t%(lineno)s\t%(msg)s'

    logging.basicConfig(filename=filename,
                        level=level,
                        filemode='a',
                        format=fmt_string,
                        datefmt='%H:%M:%S'
                        )


def _get_filename():
    local_dir = os.path.join(os.environ['RedditCode.BasePath'], 'logs')
    if not os.path.exists(local_dir):
        os.mkdir(local_dir)

    return os.path.join(local_dir, '{}.log'.format(dt.today().strftime('%Y-%m-%d')))


def _get_log_level():
    if os.environ['RedditCode.Environment'] == 'PRODUCTION':
        return logging.INFO
    elif os.environ['RedditCode.Environment'] == 'TESTING':
        return logging.DEBUG
    else:
        raise RuntimeError("No runtime environment set")


def simple_log(func):
    # TODO: log the calling module, not this one: not critical
    @functools.wraps(func)
    def wrapper(*args):
        logging.debug('Calling {}'.format(func.__qualname__))
        return func(*args)

    return wrapper
