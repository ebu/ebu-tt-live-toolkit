import logging
from .base import AbstractConsumer


log = logging.getLogger(__name__)


class LiveConsumer(AbstractConsumer):

    def start(self):
        log.info('Starting live consumer')
