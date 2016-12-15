from .interface import INode, IConsumerNode, IProducerNode
from ebu_tt_live.carriage.interface import IConsumerCarriage, IProducerCarriage
from ebu_tt_live.errors import ComponentCompatError, DataCompatError
from ebu_tt_live.strings import ERR_INCOMPATIBLE_COMPONENT, ERR_INCOMPATIBLE_DATA_EXPECTED, ERR_INCOMPATIBLE_DATA_PROVIDED


class __AbstractNode(INode):

    _node_id = None

    def __init__(self, node_id, **kwargs):
        self._node_id = node_id

    def __repr__(self):
        return '<{name}, ID:{id} at {address} >'.format(
            name=self.__class__,
            id=self._node_id,
            address=hex(id(self))
        )

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, value):
        self._node_id = value


class AbstractProducerNode(IProducerNode, __AbstractNode):

    _producer_carriage = None

    def __init__(self, node_id, producer_carriage=None, **kwargs):
        super(AbstractProducerNode, self).__init__(node_id=node_id, **kwargs)
        if producer_carriage is not None:
            self.register_producer_carriage(producer_carriage)

    def register_producer_carriage(self, producer_carriage):
        if not isinstance(producer_carriage, IProducerCarriage):
            raise ComponentCompatError(
                ERR_INCOMPATIBLE_COMPONENT.format(
                    component=producer_carriage,
                    expected_interface=IProducerCarriage
                )
            )
        if self.provides() != producer_carriage.expects():
            raise DataCompatError(
                ERR_INCOMPATIBLE_DATA_EXPECTED.format(
                    component=producer_carriage,
                    expects=producer_carriage.expects(),
                    provides=self.provides()
                )
            )
        self._producer_carriage = producer_carriage
        self._producer_carriage.register_producer_node(node=self)

    @property
    def producer_carriage(self):
        return self._producer_carriage

    def resume_producing(self):
        self.process_document(document=None)


class AbstractConsumerNode(IConsumerNode, __AbstractNode):

    _consumer_carriage = None

    def __init__(self, node_id, consumer_carriage=None, **kwargs):
        super(AbstractConsumerNode, self).__init__(node_id=node_id, **kwargs)
        if consumer_carriage is not None:
            self.register_consumer_carriage(consumer_carriage)

    def register_consumer_carriage(self, consumer_carriage):
        if not isinstance(consumer_carriage, IConsumerCarriage):
            raise ComponentCompatError(
                ERR_INCOMPATIBLE_COMPONENT.format(
                    component=consumer_carriage,
                    expected_interface=IConsumerCarriage
                )
            )
        if self.expects() != consumer_carriage.provides():
            raise DataCompatError(
                ERR_INCOMPATIBLE_DATA_EXPECTED.format(
                    component=consumer_carriage,
                    expects=consumer_carriage.provides(),
                    provides=self.expects()
                )
            )
        self._consumer_carriage = consumer_carriage
        self._consumer_carriage.register_consumer_node(node=self)

    @property
    def consumer_carriage(self):
        return self._consumer_carriage


class AbstractCombinedNode(AbstractConsumerNode, AbstractProducerNode):

    def __init__(self, node_id, producer_carriage=None, consumer_carriage=None, **kwargs):
        super(AbstractCombinedNode, self).__init__(
            node_id=node_id,
            producer_carriage=producer_carriage,
            consumer_carriage=consumer_carriage,
            **kwargs
        )
