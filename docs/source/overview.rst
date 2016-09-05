Overview of the EBU-TT live toolkit.
====================================

This page is a short introduction to using those scripts that demonstrate toolkit components. For more details and information about other scripts, follow the links below.

To run the scripts, you will need to first set up the environment and build the code. Please follow the instructions in the <a href="https://github.com/ebu/ebu-tt-live-toolkit/blob/master/README.md">README.md</a> file. 

Not all components are implemented yet - see <a href="https://github.com/ebu/ebu-tt-live-toolkit/wiki/Components">https://github.com/ebu/ebu-tt-live-toolkit/wiki/Components</a>for a list of all components. This page will be updated as more scripts are added. 

The components mimic the nodes and carriage mechanisms defined in the specification. Producer components create documents; consumer components consumer them. Each script combines a carriage mechanism implementation with a processing node to create code that can operate as a node.

Simple producer
---------------
This is a command line script. It loads static text from a file (ebu-tt-live-toolkit/ebu_tt_live/example_data/simple_producer.txt) and breaks it into a sequence of EBU-TT Live documents using natural language processing. Run it by entering the commend ``ebu-simple-producer`` without any arguments. 

The carriage mechanism is WebSocket, so you will need to listen to ``ws://127.0.0.1:9000``. Conveniently, we've created an HTML page that does just that. After you launch ``ebu-simple-producer``, open ``/ebu-tt-live-toolkit/test.html`` in your browser. The 'Broadcast message' field should be populated with the correct address (``ws://localhost:9000``). Click 'Connect' and then 'Subscribe'. You can also change the identifier for the sequence. The documents should appear in the window below.     

User input producer
-------------------
This is an advanced version of the simple producer. It adds a user interface and various configurations. First, start ``ebu-user-input-consumer`` from the command line. Then, in your browser, open ``ebu-tt-live-toolkit/ebu_tt_live/ui/user_input_producer/user_input_producer.html`` and click 'Connect'. Select a sending mode option (manual, scheduled or asynchronous). You should see the documents arrving in the command line window where ``ebu-user-input-consumer`` is listening. See detailed instrcution here: <a href="user_input_producer.html">user_input_producer.html</a>. 
TODO: confirm save to folder, e.g. ``ebu-user-input-forwarder --folder-export /xml``.





.. toctree::
    nodes_and_carriage_mechanisms
    validation
    user_input_producer
    timing_resolution
