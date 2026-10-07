
import logging
from argparse import ArgumentParser

from ebu_tt_live.documents import EBUTT3Document

from .common import create_loggers

log = logging.getLogger('ebu_interactive_shell')
parser = ArgumentParser()

parser.add_argument('-i', '--input-file', dest='input_file', default=None)


def main():
    create_loggers()
    log.info('Let\'s get started')
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, 'r') as ifile:
            document = EBUTT3Document.create_from_xml(ifile.read())

    from IPython.core.debugger import set_trace
    set_trace()
