
from ebu_tt_live.config import create_app
from .common import create_loggers


def main():
    create_loggers()
    app = create_app()
    app.start()


if __name__ == '__main__':
    main()
