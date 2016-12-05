
from ebu_tt_live.adapters.base import INodeCarriageAdapter, IDocumentDataAdapter
from ebu_tt_live.adapters.node_carriage import AbstractNodeCarriageAdapter, ProducerNodeCarriageAdapter, \
    ConsumerNodeCarriageAdapter
from ebu_tt_live.node import IConsumerNode, IProducerNode, SimpleProducer, SimpleConsumer
from ebu_tt_live.carriage import IConsumerCarriage, IProducerCarriage, FilesystemConsumerImpl, FilesystemProducerImpl, \
    WebsocketConsumerCarriage, WebsocketProducerCarriage
from ebu_tt_live.errors import DataCompatError
from unittest import TestCase
import pytest


class CustomDataType1(object):
    pass


class CustomDataType2(object):
    pass


def test_abs_instantiate():
    with pytest.raises(TypeError):
        AbstractNodeCarriageAdapter()


@pytest.fixture
def consumer_carriage(mocker):
    carr = mocker.MagicMock(spec=IConsumerCarriage)
    carr.provides.return_value = CustomDataType1
    return carr


@pytest.fixture
def producer_carriage(mocker):
    carr = mocker.MagicMock(spec=IProducerCarriage)
    carr.expects.return_value = CustomDataType1
    return carr


@pytest.fixture
def consumer_node(mocker):
    cons = mocker.MagicMock(spec=IConsumerNode)
    cons.expects.return_value = CustomDataType1

    def register_consumer_carriage(carr):
        carr.register_consumer_node(cons)

    cons.register_consumer_carriage.side_effect = register_consumer_carriage
    return cons


@pytest.fixture
def producer_node(mocker):
    prod = mocker.MagicMock(spec=IProducerNode)
    prod.provides.return_value = CustomDataType1

    def register_producer_carriage(carr):
        carr.register_producer_node(prod)

    prod.register_producer_carriage.side_effect = register_producer_carriage
    return prod


@pytest.fixture(autouse=True)
def get_document_data_adapter(mocker):

    def mock_gdda(expects, provides):

        def dummy_convert(data, **kwargs):
            return mocker.MagicMock(spec=provides), kwargs

        dda = mocker.MagicMock(spec=IDocumentDataAdapter)
        dda.expects.return_value = expects
        dda.provides.return_value = provides
        dda.convert_data.side_effect = dummy_convert
        return dda

    gdda = mocker.patch('ebu_tt_live.adapters.node_carriage.get_document_data_adapter')
    gdda.side_effect = mock_gdda
    return gdda


@pytest.fixture
def consumer_carriage_adapter(consumer_carriage, consumer_node, get_document_data_adapter):
    cca = ConsumerNodeCarriageAdapter(
        consumer_carriage=consumer_carriage,
        consumer_node=consumer_node
    )
    return cca


@pytest.fixture
def producer_carriage_adapter(producer_carriage, producer_node, get_document_data_adapter):
    dda = ProducerNodeCarriageAdapter(
        producer_carriage=producer_carriage,
        producer_node=producer_node
    )
    return dda


def test_cca_instantiate(consumer_carriage, consumer_node, get_document_data_adapter):
    instance = ConsumerNodeCarriageAdapter(
        consumer_carriage=consumer_carriage,
        consumer_node=consumer_node
    )
    assert isinstance(instance, IConsumerNode)
    assert isinstance(instance, IConsumerCarriage)
    get_document_data_adapter.assert_not_called()
    assert len(instance.data_adapters) == 0


def test_cca_data_adapters_custom_success(mocker, consumer_carriage, consumer_node, get_document_data_adapter):
    consumer_node.expects.return_value = CustomDataType2
    dda = mocker.MagicMock(spec=IDocumentDataAdapter)
    dda.expects.return_value = CustomDataType1
    dda.provides.return_value = CustomDataType2
    instance = ConsumerNodeCarriageAdapter(
        consumer_carriage=consumer_carriage,
        consumer_node=consumer_node,
        data_adapters=[dda]
    )
    get_document_data_adapter.assert_not_called()
    assert instance.data_adapters == [dda]
    dda.convert_data.assert_not_called()
    consumer_carriage.register_consumer_node.assert_called_once()
    consumer_node.register_consumer_carriage.assert_called_once()


def test_cca_data_adapters_custom_error_empty_param(mocker, consumer_carriage, consumer_node):
    consumer_node.expects.return_value = CustomDataType2

    with pytest.raises(DataCompatError):
        instance = ConsumerNodeCarriageAdapter(
            consumer_carriage=consumer_carriage,
            consumer_node=consumer_node,
            data_adapters=[]
        )

def test_cca_data_adapters_custom_error_incompatible_param(mocker, consumer_carriage, consumer_node):
    consumer_node.expects.return_value = CustomDataType2
    dda = mocker.MagicMock(spec=IDocumentDataAdapter)
    dda.expects.return_value = CustomDataType1
    dda.provides.return_value = CustomDataType1

    with pytest.raises(DataCompatError):
        instance = ConsumerNodeCarriageAdapter(
            consumer_carriage=consumer_carriage,
            consumer_node=consumer_node,
            data_adapters=[dda]
        )


def test_cca_data_adapters_auto_error_incompatible_param(consumer_carriage, consumer_node, get_document_data_adapter):
    consumer_node.expects.return_value = CustomDataType2

    get_document_data_adapter.side_effect = ValueError

    with pytest.raises(DataCompatError):
        instance = ConsumerNodeCarriageAdapter(
            consumer_carriage=consumer_carriage,
            consumer_node=consumer_node
        )


def test_cca_data_adapters_auto(consumer_carriage, consumer_node, get_document_data_adapter):
    consumer_node.expects.return_value = CustomDataType2
    instance = ConsumerNodeCarriageAdapter(
        consumer_carriage=consumer_carriage,
        consumer_node=consumer_node
    )
    get_document_data_adapter.assert_called_once()
    get_document_data_adapter.assert_called_with(expects=CustomDataType1, provides=CustomDataType2)


def test_cca_conversion_data_passthrough(mocker, consumer_carriage, consumer_node, consumer_carriage_adapter):
    data = mocker.MagicMock(spec=CustomDataType1)

    consumer_node.process_document.assert_not_called()

    consumer_carriage_adapter.process_document(document=data)

    consumer_node.process_document.assert_called_once()


def test_cca_conversion_data_convert(mocker, consumer_carriage, consumer_node):
    data = mocker.MagicMock(spec=CustomDataType1)
    consumer_node.expects.return_value = CustomDataType2
    cca = ConsumerNodeCarriageAdapter(
        consumer_carriage=consumer_carriage,
        consumer_node=consumer_node
    )

    consumer_node.process_document.assert_not_called()
    cca.data_adapters[0].convert_data.assert_not_called()

    cca.process_document(document=data)

    cca.data_adapters[0].convert_data.assert_called_once()
    cca.data_adapters[0].convert_data.assert_called_with(data)
    consumer_node.process_document.assert_called_once()


def test_pca_instantiate(producer_carriage, producer_node, get_document_data_adapter):
    instance = ProducerNodeCarriageAdapter(
        producer_node=producer_node,
        producer_carriage=producer_carriage
    )
    assert isinstance(instance, IProducerNode)
    assert isinstance(instance, IProducerCarriage)
    get_document_data_adapter.assert_not_called()
    assert len(instance.data_adapters) == 0


def test_pca_data_adapters_custom_success(mocker, producer_carriage, producer_node, get_document_data_adapter):
    producer_carriage.expects.return_value = CustomDataType2
    dda = mocker.MagicMock(spec=IDocumentDataAdapter)
    dda.expects.return_value = CustomDataType1
    dda.provides.return_value = CustomDataType2
    instance = ProducerNodeCarriageAdapter(
        producer_carriage=producer_carriage,
        producer_node=producer_node,
        data_adapters=[dda]
    )
    get_document_data_adapter.assert_not_called()
    assert instance.data_adapters == [dda]
    dda.convert_data.assert_not_called()
    producer_carriage.register_producer_node.assert_called_once()
    producer_node.register_producer_carriage.assert_called_once()


def test_pca_data_adapters_auto(producer_carriage, producer_node, get_document_data_adapter):
    producer_carriage.expects.return_value = CustomDataType2
    instance = ProducerNodeCarriageAdapter(
        producer_node=producer_node,
        producer_carriage=producer_carriage
    )
    get_document_data_adapter.assert_called_once()
    get_document_data_adapter.assert_called_with(expects=CustomDataType1, provides=CustomDataType2)


def test_pca_conversion_data_passthrough(mocker, producer_carriage, producer_node, producer_carriage_adapter):
    data = mocker.MagicMock(spec=CustomDataType1)

    producer_carriage.emit_data.assert_not_called()

    producer_carriage_adapter.emit_data(data=data)

    producer_carriage.emit_data.assert_called_once()
