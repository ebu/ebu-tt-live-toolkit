
from pytest import fixture, raises
from ebu_tt_live.config import AppConfig
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
                        "uri": "ws://localhost:9001"
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
                        "uri": "ws://localhost:9000/TestSequence2"
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
                        "uri": "ws://localhost:9000/TestSequence2"
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
