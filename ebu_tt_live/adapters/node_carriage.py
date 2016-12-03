
from .base import INodeCarriageAdapter
from ebu_tt_live.carriage.interface import IProducerCarriage, IConsumerCarriage
from ebu_tt_live.node.interface import IProducerNode, IConsumerNode
from ebu_tt_live.errors import DataCompatError
from ebu_tt_live.strings import ERR_INCOMPATIBLE_DATA_CONVERSION
from .document_data import get_document_data_adapter
from ebu_tt_live.utils import ANY



class AbstractNodeCarriageAdapter(INodeCarriageAdapter):

    _data_adapters = None

    @property
    def data_adapters(self):
        return self._data_adapters

    def _set_data_adapters(self, value, expects, provides):
        success = True

        if value:
            data_adapters = list(value)
        elif expects != provides:
            try:
                data_adapters = [get_document_data_adapter(
                    provides=expects,
                    expects=provides
                )]
                # It managed to find an adapter :)
                success = True
            except ValueError as exc:
                success = False
                data_adapters = []
        else:
            data_adapters = []

        if len(data_adapters):
            if data_adapters[0].expects() != provides or data_adapters[-1].provides() != expects:
                success = False
        elif expects == provides:
            success = True
        else:
            success = False

        if success is False:
            raise DataCompatError(
                ERR_INCOMPATIBLE_DATA_CONVERSION.format(
                    expects=provides,
                    provides=expects
                )
            )

        self._data_adapters = data_adapters

    def convert_data(self, data, **kwargs):
        in_kwargs = {}
        in_kwargs.update(kwargs)
        in_data = data
        for data_adapter in self.data_adapters:
            in_data, in_kwargs = data_adapter.convert_data(in_data, **in_kwargs)
        return in_data, in_kwargs


class ProducerNodeCarriageAdapter(IProducerCarriage, IProducerNode, AbstractNodeCarriageAdapter):

    _producer_node = None
    _producer_carriage = None
    _expects = ANY
    _provides = ANY

    def __init__(self, producer_node, producer_carriage, data_adapters=None):
        self._expects = producer_node.provides()
        self._provides = producer_carriage.expects()

        self._set_data_adapters(
            value=data_adapters,
            expects=self.provides(),
            provides=self.expects()
        )
        self.register_producer_carriage(producer_carriage)
        # This will in turn call our register_producer_node method back.
        producer_node.register_producer_carriage(self)

    def register_producer_carriage(self, producer_carriage):
        # We don't have to revalidate the interfaces as they are done on both sides for us
        self._producer_carriage = producer_carriage
        self._producer_carriage.register_producer_node(self)

    def register_producer_node(self, node):
        self._producer_node = node

    def expects(self):
        return self._expects

    def provides(self):
        return self._provides

    @property
    def producer_carriage(self):
        return self._producer_carriage

    @property
    def producer_node(self):
        return self._producer_node

    def resume_producing(self):
        self.producer_node.resume_producing()

    def emit_data(self, data, **kwargs):
        # Conversion happens here in this traffic direction
        conv_data, new_kwargs = self.convert_data(data, **kwargs)
        self.producer_carriage.emit_data(conv_data, **new_kwargs)

    def process_document(self, document, **kwargs):
        # a producer carriage mechanism is not supposed to call this function
        self.producer_node.process_document(document=document, **kwargs)


class ConsumerNodeCarriageAdapter(IConsumerNode, IConsumerCarriage, AbstractNodeCarriageAdapter):

    _consumer_carriage = None
    _consumer_node = None
    _expects = ANY
    _provides = ANY

    def __init__(self, consumer_node, consumer_carriage, data_adapters=None):
        self._expects = consumer_carriage.provides()
        self._provides = consumer_node.expects()

        self._set_data_adapters(
            value=data_adapters,
            provides=self.expects(),
            expects=self.provides()
        )
        self.register_consumer_carriage(consumer_carriage)
        # This will in turn call our register_consumer_node method back.
        consumer_node.register_consumer_carriage(self)

    def register_consumer_carriage(self, consumer_carriage):
        self._consumer_carriage = consumer_carriage
        self._consumer_carriage.register_consumer_node(self)

    def register_consumer_node(self, node):
        self._consumer_node = node

    def expects(self):
        return self._expects

    def provides(self):
        return self._provides

    @property
    def consumer_carriage(self):
        return self._consumer_carriage

    @property
    def consumer_node(self):
        return self._consumer_node

    def on_new_data(self, data, **kwargs):
        # Again in this scenario this is unlikely to be called by anyone
        self.consumer_node.on_new_data(data, **kwargs)

    def process_document(self, document, **kwargs):
        # Conversion happens here in this traffic direction
        conv_doc, new_kwargs = self.convert_data(document, **kwargs)
        self.consumer_node.process_document(conv_doc, **new_kwargs)
