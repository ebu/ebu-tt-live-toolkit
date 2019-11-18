Overview of the EBU-TT live toolkit.
====================================

This page is a short introduction to using those scripts that demonstrate toolkit components. For more details and information about other scripts, follow the links below.

To run the scripts, you will need to first set up the environment and build the code. Please follow the instructions in https://github.com/ebu/ebu-tt-live-toolkit/blob/master/README.md.

Not all components are implemented yet - see https://github.com/ebu/ebu-tt-live-toolkit/wiki/Components for a list of all components. This page will be updated as more scripts are added.

The components mimic the nodes and carriage mechanisms defined in the specification. Producer components create documents; consumer components consume them. Each script combines a carriage mechanism implementation with a processing node to create code that can operate as a node.

.. toctree::
    nodes_and_carriage_mechanisms
    scripts_and_their_functions
    configurator
    validation
    user_input_producer
    timing_resolution
    segmentation
    deduplication
    denesting
    conversion_from_ebutt
    conversion_to_ebuttd
