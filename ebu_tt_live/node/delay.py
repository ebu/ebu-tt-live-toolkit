from .base import Node

class FixedDelayNode(Node):

	_reference_clock = None
	_sequence = None

	def __init__(self, node_id, carriage_impl, reference_clock):
		super(FixedDelayNode, self).__init__(node_id, carriage_impl)
		self._reference_clock = reference_clock

	def process_document(self, document):

		pass