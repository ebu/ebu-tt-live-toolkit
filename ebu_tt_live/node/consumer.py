
from .base import ConsumerNode
from datetime import timedelta
import logging


log = logging.getLogger(__name__)


class SimpleConsumer(ConsumerNode):

    def __init__(self, node_id):
        super(SimpleConsumer, self).__init__(node_id)

    def process_document(self, document):
        log.info(document)
