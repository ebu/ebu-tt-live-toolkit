"""
The ``ebu-run`` script is a universal runner for any component or complex interconnected sets of components
based on a compliant configuration file or set of valid options. The configuration framework uses
the mozilla/configman package that picks up configuration from command line/config file.

Basic usage:
------------

  ::

    ebu-run --admin.conf=ebu_tt_live/examples/config/simple-producer.json

Adjust existing config file:
----------------------------

  ::

    ebu-run --admin.conf=ebu_tt_live/examples/config/simple-producer.json --nodes.node1.sequence_identifier=Sequence2

Help:
-----

  ::

    ebu-run --admin.conf=ebu_tt_live/examples/config/simple-producer.json --help

The --help flag aims to be context matching so anywhere as long as configman is used is expected and it elaborates
the directly accessible config file keys using the current configuration structure as well as possible alternative
values for the keys already having a value from the config file or from the command line.

Since the components and their connections are not hard-coded the ``ebu-run`` does not have a single purpose
limitation. The usage of a configrator facilitates the configuration mapping of a single node or an entire complex
interconnected set of nodes via various carriage mechanisms, events and timings.
"""

from ebu_tt_live.config import create_app
from .common import create_loggers


def main():
    create_loggers()
    app = create_app()
    app.start()


if __name__ == '__main__':
    main()
