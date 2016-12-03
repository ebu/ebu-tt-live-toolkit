
from .common import ConfigurableComponent
from configman import RequiredConfig, Namespace, converters
from ebu_tt_live.adapters import document_data, node_carriage


def data_adapters_by_directed_conversion(data_adapter):
    if data_adapter == 'xml->ebutt3':
        return document_data.XMLtoEBUTT3Adapter
    elif data_adapter == 'xml->ebuttd':
        return document_data.XMLtoEBUTTDAdapter
    elif data_adapter == 'ebutt3->xml':
        return document_data.EBUTT3toXMLAdapter
    elif data_adapter == 'ebuttd->xml':
        return document_data.EBUTTDtoXMLAdapter


def parse_adapter_list(value):
    # This is working around a bug that configman leaves the lists intact
    parsed_value = []
    if value is not None:
        for item in value:
            conv_type = item['type']
            kwargs = {ckey: carg for ckey, carg in item.items() if ckey != 'type'}
            parsed_value.append(data_adapters_by_directed_conversion(conv_type)(**kwargs))
    return parsed_value


class ProducerNodeCarriageAdapter(ConfigurableComponent):

    @classmethod
    def configure_component(cls, config, local_config, producer=None, carriage=None, **kwargs):
        instance = cls(config=config, local_config=local_config)
        adapter_list = parse_adapter_list(local_config)
        instance.component = node_carriage.ProducerNodeCarriageAdapter(
            producer_carriage=carriage,
            producer_node=producer,
            data_adapters=adapter_list
        )


class ConsumerNodeCarriageAdapter(ConfigurableComponent):

    @classmethod
    def configure_component(cls, config, local_config, consumer=None, carriage=None, **kwargs):
        instance = cls(config=config, local_config=local_config)
        adapter_list = parse_adapter_list(local_config)
        instance.component = node_carriage.ConsumerNodeCarriageAdapter(
            consumer_carriage=carriage,
            consumer_node=consumer,
            data_adapters=adapter_list
        )
