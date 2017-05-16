Scripts and their functions
===========================

The ebu-run script
------------------
This script is capable of picking up a structured configuration file and use
that to create the nodes and carriage mechanism objects that we would like to
use/ They can be even wired in the same configuration file together so in the
end a complex system can be modeled using a single json file. Please refer to
:py:mod:`ebu_tt_live.scripts.ebu_run` as well as :py:mod:`ebu_tt_live.config` to
learn more about the way the configuration logic works. To get help on permitted
options for the specified node(s) run ``ebu-run`` with a ``--help``. See
:doc:`configurator`.

Simple Producer
---------------
This script loads static text from a file
(``ebu-tt-live-toolkit/ebu_tt_live/examples/simple_producer.txt``) and breaks it
into a sequence of EBU-TT Live documents using natural language processing. Use ``ebu-run`` to start it:
``ebu-run --admin.conf=ebu_tt_live/examples/config/simple_producer.json``

The default carriage mechanism is WebSocket, so you will need to listen to
``ws://127.0.0.1:9000``. Conveniently, we've created an HTML page that does just
that. After you launch the Simple Producer, open ``test.html`` in your
browser. The 'Broadcast message' field should be populated with the correct
address (``ws://localhost:9000``). Click 'Connect' and then 'Subscribe'. You can
also change the identifier for the sequence. The documents should appear in the
window below.

Alternatively, the Simple Producer can use the file system as the carriage
mechanism. To do this, create a configuration file and specify the carriage mechanism
and output folder options as described in `<configurator.html>`__ .
This saves the documents in the specified output folder together
with a manifest file that can be used by the Simple Consumer (below). See
`<filesystem_carriage_mechanism.html>`__ for more details about the file system
carriage mechanism.

Simple consumer
---------------
This script reads and validates documents in a sequence. It performs both
semantic and syntactic validation of the XML. By default, it uses WebSocket and
listens to ``ws://localhost:9000``. To start this default configuration, run
``ebu-run --admin.conf=ebu_tt_live/examples/config/simple_consumer.json``.
You can also point the Simple Consumer to the file system. If you saved the documents
in a folder (using the folder export configuration option
of the Simple Producer), you can write a configuration file with as
described in `<configurator.html>`__ and pass this file to ``ebu-run``.

User Input Producer
-------------------
This is a web page that adds a user interface and various configurations to the
Simple Producer. First, start a consumer or a handover node as described above. Then, in your browser, open
``ebu_tt_live/ui/user_input_producer/user_input_producer.html`` and click
'Connect'. Select the sending mode (manual, scheduled or asynchronous). You
should see the documents arriving in the command line window where
``ebu-user-input-consumer`` is listening. You can also view the documents within the UIP page. See detailed instructions here:
:doc:`user_input_producer`.

User Input Consumer
-------------------
This is very similar to the Simple Consumer. It also performs validation but it
does not have a manifest option. It provides a WebSocket connection point for
the User Input Producer. You'll need to start either this or the User Input
Forwarder before connecting the User Input Producer (but not both).

Distributor
-----------
This script mimics a distribution node. To see it forwarding documents from the Simple Producer the the Simple Consumer using Websocket, run ``ebu-run --admin.conf=ebu_tt_live/examples/config/sproducer_dist_sconsumer_ws.json``. A more interesting scenario is distributing documents from the User Input Producer to two consumer nodes: ``ebu-run --admin.conf=ebu_tt_live/examples/config/user_input_producer_dist_consumers``.

Like the Simple Producer, the Distributor can also save the documents it receives to the file system. To do that, create you own configuration file as described in `<configurator.html>`__ and pass this file to ``ebu-run``.

Handover Manager
----------------
This node implements the 'Who claimed control most recently' algorithm defined
in the specification, with added functionality to allow messages to be broadcast
between members of the authors group, which may be added to a future
specification. This algorithm determines the output from multiple input
sequences. The Handover Manager is a specialised case of the switching node that
bases its decisions on handover-related attributes in the document and its
previous decisions. There is no separate command to run this script. Start it
with the ``ebu-run``, for example ``ebu-run
--admin.conf=ebu_tt_live/examples/config/user_input_producer_handover.json`` for
the default configuration. For detailed instruction on setting up the Handover
Manager with the UIP see :doc:`user_input_producer`.

EBU-TT-D Encoder
----------------
This script is an extension of simple consumer and is responsible for
resegmenting and converting the incoming EBU-TT Live documents into EBU-TT-D
documents that can be later used to be embedded in video streams such as DASH. There are configuration file options for controlling the media time conversion reference point and the segmentation interval; these are described in `<configurator.html>`__.

To see the Encoder in action, using output from the Simple Producer and the 'direct' carriage mechanism, run ``ebu-run
--admin.conf=ebu_tt_live/examples/config/sproducer_ebuttd_direct.json``.

IMPORTANT: the Encoder is not a complete EBU-TT Live to EBU-TT-D converter. Since EBU-TT-D generation was not part of this project, this functionality was implemented only partially and should not be used as reference.
