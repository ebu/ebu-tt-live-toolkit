Configuration files and ``ebu-run``
===================================

There are 2 ways the nodes and carriage mechanisms can be set up:

    1. Write a script where you instantiate these components and connect them. This technique is making use of
    dependency injection. This means the nodes and carriage mechanisms do not need to know about the creation of
    each other. They just get the already created component referenced as a parameter, and check if that component
    implement the expected interface. This eliminates the possibility of creating spaghetti code where a node would know
    how to create a carriage mechanism and deal with all the possible parameters and a carriage mechanism would know
    in turn how to instantiate a node. This is to be avoided. And this brings us to the second way to do this.

    2. Use the component configurators and use a simple configuration file to create your system and give the
    configuration file to the :py:mod:`ebu_tt_live.scripts.ebu_run` script, which takes care of creating all the
    required components for you. This eliminates the need for a programmer to keep repeating the configuration logic
    in their scripts where they create the components.

The idea is the following: The components(nodes, carriage mechanisms, converters, resegmenters...etc.) are agnostic
to one another as long as the carriage mechanism is capable of transporting the payload the node expects. But their
wiring and their factories are actually the configurator classes. The configurator class defines the type and
name of the configuration options relevant to the component and wires it with its immediate dependencies. This
way the factories that create the system are separate from the system's business logic and this separation is
meant to be kept. There is a simple naming correspondence. For instance the business logic of the processing
nodes are in the :py:mod:`ebu_tt_live.node` package while their configurators are to be found in the
:py:mod:`ebu_tt_live.config.node` module.

The configuration file structure
--------------------------------

The configuration file is JSON at the moment. The general structure looks like this:

    ::

        {
            "nodes": {
                "node1": {
                    "type": "simple-producer",
                    "output": { ... }
                    ...
                },
                "node2": { ... },
                ...
            },
            "backend": {
                "type": "twisted",
                ...
            }
        }

The nodes are supposed to be compatible with the chosen backend. The backend object is instantiated first and
every component configurator has access to the backend that was created and it is their responsibility to
ensure that compatibility is checked with the backend. The backend is meant to be giving a framework for
timing things, network stack access, threading...etc. Different backends may offer different features and if
a component configurator is not compatible with the backend object it is supposed to raise a ConfigurationError.

The node contains either an input or an output section or both in case it is a node that is a consumer and a
producer at the same time, like a forwarder node, a handover node, a converter...etc. The input and output bits
define the carriage mechanism that that side is supposed to be talking to. So providing 2 nodes a producer with
an output carriage mechanism of a websocket and a consumer of an input carriage mechanism of the same websocket
address that the producer is using essentially creates a loopback through the network stack between the 2 nodes
and they will talk to one another. An even more convenient way of doing the same thing is to use
the carriage mechanism type: ``direct``
Please refer to the :py:mod:`ebu_tt_live.scripts.ebu_run` for more information.
