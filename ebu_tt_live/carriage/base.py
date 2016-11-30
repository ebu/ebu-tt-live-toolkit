from .interface import IProducerCarriage, IConsumerCarriage
from ebu_tt_live.node.interface import IProducerNode, IConsumerNode
from ebu_tt_live.errors import ComponentCompatError, DataCompatError
from ebu_tt_live.strings import ERR_INCOMPATIBLE_COMPONENT, ERR_INCOMPATIBLE_DATA_EXPECTED, \
    ERR_INCOMPATIBLE_DATA_PROVIDED

# Abstract classes
# ================


class AbstractProducerCarriage(IProducerCarriage):

    _producer_node = None

    def register_producer_node(self, node):
        if not isinstance(node, IProducerNode):
            raise ComponentCompatError(
                ERR_INCOMPATIBLE_COMPONENT.format(
                    component=node,
                    expected_interface=IProducerNode
                )
            )
        if self.expects() != node.provides():
            raise DataCompatError(
                ERR_INCOMPATIBLE_DATA_EXPECTED.format(
                    component=node,
                    expects=self.expects(),
                    provides=node.provides()
                )
            )
        self._producer_node = node

    @property
    def producer_node(self):
        return self._producer_node

    def resume_producing(self):
        self.producer_node.resume_producing()


class AbstractConsumerCarriage(IConsumerCarriage):

    _consumer_node = None

    def register_consumer_node(self, node):
        if not isinstance(node, IConsumerNode):
            raise ComponentCompatError(
                ERR_INCOMPATIBLE_COMPONENT.format(
                    component=node,
                    expected_interface=IConsumerNode
                )
            )
        if self.provides() != node.expects():
            raise DataCompatError(
                ERR_INCOMPATIBLE_DATA_PROVIDED.format(
                    component=node,
                    expects=node.expects(),
                    provides=self.provides()
                )
            )
        self._consumer_node = node

    @property
    def consumer_node(self):
        return self._consumer_node


class AbstractCombinedCarriage(AbstractConsumerCarriage, AbstractProducerCarriage):
    pass
