
from .base import Node
from datetime import timedelta
import logging


log = logging.getLogger(__name__)


class SimpleConsumer(Node):

    def __init__(self, node_id, carriage_impl):
        super(SimpleConsumer, self).__init__(node_id, carriage_impl)

    def process_document(self, document):
        log.info(document._ebutt3_content.body.begin.timedelta)
