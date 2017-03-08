
from pytest import fixture, raises
from ebu_tt_live.config import AppConfig, UniversalNodes
import ebu_tt_live.config.node as node_config
import ebu_tt_live.config.carriage as carriage_config
import ebu_tt_live.node as processing_node
from ebu_tt_live.config.common import ConfigurableComponent
from ebu_tt_live.errors import ConfigurationError


@fixture(autouse=True)
def reset_backend():
    # This fixture makes sure the backend reference deleted before every test
    ConfigurableComponent._backend = None


def test_simple_producer():

    val_source = {
        "nodes": {
            "node1": {
                "id": "producer1",
                "type": "simple-producer",
                "show_time": True,
                "sequence_identifier": "TestSequence1",
                "output": {
                    "carriage": {
                        "type": "direct",
                        "id": "default"
                    }
                }
            }
        },
        "backend": {
            "type": "dummy"
        }
    }

    app = AppConfig(
        values_source_list=[val_source]
    )

    app.start()


def test_handover_conf():

    val_source = {
        "nodes": {
            "node1": {
                "id": "handover1",
                "type": "handover",
                "authors_group_identifier": "TestGroup1",
                "sequence_identifier": "TestSequence1",
                "input": {
                    "carriage": {
                        "type": "direct",
                        "id": "default_in"
                    }
                },
                "output": {
                    "carriage": {
                        "type": "direct",
                        "id": "default_out"
                    }
                }
            }
        },
        "backend": {
            "type": "dummy"
        }
    }

    app = AppConfig(
        values_source_list=[val_source]
    )

    app.start()

    created_node_configurator = app.get_node("node1")

    assert isinstance(created_node_configurator, node_config.Handover)
    assert isinstance(created_node_configurator.component, processing_node.HandoverNode)
    assert created_node_configurator.component._sequence_identifier == 'TestSequence1'
    assert created_node_configurator.component._authors_group_identifier == 'TestGroup1'
    assert isinstance(created_node_configurator._input.carriage, carriage_config.DirectInput)
    assert isinstance(created_node_configurator.output.carriage, carriage_config.DirectOutput)


def test_simple_producer_wrong_backend():
    val_source = {
        "nodes": {
            "node1": {
                "id": "producer1",
                "type": "simple-producer",
                "show_time": True,
                "sequence_identifier": "TestSequence1",
                "output": {
                    "carriage": {
                        "type": "websocket",
                        "listen": "ws://localhost:9001"
                    }
                }
            }
        },
        "backend": {
            "type": "dummy"
        }
    }

    app = AppConfig(
        values_source_list=[val_source]
    )
    with raises(AttributeError):
        app.start()


def test_simple_consumer():
    val_source = {
        "nodes": {
            "node1": {
                "id": "consumer1",
                "type": "simple-consumer",
                "input": {
                    "carriage": {
                        "type": "direct",
                        "id": "default"
                    }
                }
            }
        },
        "backend": {
            "type": "dummy"
        }
    }

    app = AppConfig(
        values_source_list=[val_source]
    )
    app.start()


def test_simple_consumer_wrong_backend():
    val_source = {
        "nodes": {
            "node1": {
                "id": "consumer1",
                "type": "simple-consumer",
                "input": {
                    "carriage": {
                        "type": "websocket",
                        "connect": ["ws://localhost:9000/TestSequence2/subscribe"]
                    }
                }
            }
        },
        "backend": {
            "type": "dummy"
        }
    }

    app = AppConfig(
        values_source_list=[val_source]
    )
    with raises(AttributeError):
        app.start()


def test_wrong_node_type():
    val_source = {
        "nodes": {
            "node1": {
                "id": "consumer1",
                "type": "no-such-consumer",
                "input": {
                    "carriage": {
                        "type": "websocket",
                        "connect": ["ws://localhost:9000/TestSequence2/subscribe"]
                    }
                }
            }
        },
        "backend": {
            "type": "dummy"
        }
    }

    with raises(ConfigurationError):
        app = AppConfig(
            values_source_list=[val_source]
        )

        app.start()
