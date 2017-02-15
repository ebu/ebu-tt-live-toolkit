import logging
import re

from twisted.python import log as twisted_log

log = logging.getLogger(__name__)
log_format = '[%(levelname)s] (%(asctime)s) in %(name)s[%(lineno)d] - %(message)s'
yaml_file = re.compile('^.*(\.yml|\.yaml)(\w)?$')


def create_loggers(level=logging.INFO):
    # Pipe Twisted's loggers into python logging package
    log_observer = twisted_log.PythonLoggingObserver()
    log_observer.start()
    # Python logging setup
    # TODO: Make this configurable (https://github.com/bbc/ebu-tt-live-toolkit/issues/15)
    logging.basicConfig(level=level, format=log_format)
