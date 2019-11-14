Scripts and their functions
===========================

The ebu-run script
------------------
This script is capable of picking up a structured configuration file and use
that to create the nodes and carriage mechanism objects that we would like to
use. They can be even wired in the same configuration file together so in the
end a complex system can be modeled using a single json file. Please refer to
:py:mod:`ebu_tt_live.scripts.ebu_run` as well as :py:mod:`ebu_tt_live.config` to
learn more about the way the configuration logic works. To get help on permitted
options for the specified node(s) run ``ebu-run`` with a ``--help``. See
:doc:`configurator`.

Simple Producer
---------------
This script loads static text from a file
(``ebu-tt-live-toolkit/ebu_tt_live/examples/simple_producer.txt``) and breaks it
into a sequence of EBU-TT Live documents using natural language processing. Use
``ebu-run`` to start it: ``ebu-run
--admin.conf=ebu_tt_live/examples/config/simple_producer.json``

The default carriage mechanism is WebSocket, so you will need to listen to
``ws://127.0.0.1:9000``. Conveniently, we've created an HTML page that does just
that. After you launch the Simple Producer, open `docs/build/ui/test/index.html <../ui/test/index.html>`_
or the `current release pre-built page <http://ebu.github.io/ebu-tt-live-toolkit/ui/test/>`_ in your
browser. The 'Broadcast message' field should be populated with the correct
address (``ws://localhost:9000``). Click 'Connect' and then 'Subscribe'. You can
also change the identifier for the sequence. The documents should appear in the
window below.

Alternatively, the Simple Producer can use the file system as the carriage
mechanism. To do this, create a configuration file and specify the carriage
mechanism and output folder options as described in :doc:`configurator` . This
saves the documents in the specified output folder together with a manifest file
that can be used by the Simple Consumer (below). See
:doc:`filesystem_carriage_mechanism` for more details about the file system
carriage mechanism.

Simple consumer
---------------
This script reads and validates documents in a sequence. It performs both
semantic and syntactic validation of the XML. By default, it uses WebSocket and
listens to ``ws://localhost:9000``. To start this default configuration, run
``ebu-run --admin.conf=ebu_tt_live/examples/config/simple_consumer.json``.
You can also point the Simple Consumer to the file system. If you saved the documents
in a folder (using the folder export configuration option
of the Simple Producer), you can write a configuration file as
described in :doc:`configurator` and pass this file to ``ebu-run``.

User Input Producer
-------------------
This is a web page that adds a user interface and various configurations to the
Simple Producer. It needs to connect to a node that can receive incoming
``/publish`` style WebSocket connections, for example a Simple Consumer, a
Distributor or a Handover Manager Node. First, with your virtual environment
activated and the code built, start one, with a command line such as  ``ebu-run
--admin.conf ebu_tt_live/examples/config/user_input_producer_consumer.json`` -
this one runs a simple consumer. Then, in your browser, open
`docs/build/ui/user_input_producer/index.html <../ui/user_input_producer/index.html>`_ or the
`current release pre-built page <http://ebu.github.io/ebu-tt-live-toolkit/ui/user_input_producer/>`_ and click
'Connect'. Select the sending mode (manual, scheduled or asynchronous). You
should see the documents arriving in the command line window where the simple
consumer is listening. See detailed instructions here:
:doc:`user_input_producer`.

Distributor
-----------
This script mimics a distribution node. To see it forwarding documents from the
Simple Producer the the Simple Consumer using Websocket, run ``ebu-run
--admin.conf=ebu_tt_live/examples/config/sproducer_dist_sconsumer_ws.json``. A
more interesting scenario is distributing documents from the User Input Producer
to two consumer nodes: ``ebu-run
--admin.conf=ebu_tt_live/examples/config/user_input_producer_dist_consumers``.

Like the Simple Producer, the Distributor can also save the documents it
receives to the file system. To do that, create you own configuration file as
described in :doc:`configurator` and pass this file to ``ebu-run``.

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

Buffer Delay Node
-----------------
This script buffers each received Document and emits it after a fixed
non-negative delay offset period. Since this is a passive node, essentially
equivalent to a longer carriage latency, no modification to the documents is
required. The Buffer Delay Node is primarily intended for delaying implicitly
timed documents for resynchronisation. Use ``ebu-run`` to start this script, for
example ``ebu-run --admin.conf=ebu_tt_live/examples/config/buffer_delay.json``

DeDuplicator Node
-----------------
This node addresses instances where ``style`` and ``region`` elements and
attributes are duplicated.
For the default configuration of the node, see:
``ebu-run --admin.conf=ebu_tt_live/examples/config/deduplicator_fs.json``

Denester Node
-------------
This node flattens nested ``div`` and ``span`` elements such that no
``div`` ends up containing a ``div`` and no ``span`` ends up containing
a ``span``. It also removes any ``p`` elements that specify a ``region``
attribute that differs from a specified region on an ancester element.

If nested ``div`` or ``span`` elements might be present in a document, the
Denester node should be used to flatten them before passing them to the
EBU-TT-D Encoder, because EBU-TT-D does not permit such nested elements.

Retiming Delay Node
-------------------
This script modifies the times within each Document and issues them without
further emission delay as part of a new sequence with a new sequence identifier.
The times are modified such that all of the computed begin and end times within
the document are increased by a non-negative fixed delay offset period. The
Retiming Delay Node is primarily intended for delaying explicitly timed
documents. Use ``ebu-run`` to start this script, for example ``ebu-run
--admin.conf=ebu_tt_live/examples/config/retiming_delay.json.``

EBU-TT-D Encoder
----------------
This script is an extension of simple consumer and is responsible for
resegmenting and converting the incoming EBU-TT Live documents into EBU-TT-D
documents that can be later used to be embedded in video streams such as DASH.
There are configuration file options for controlling the media time conversion
reference point and the segmentation interval; these are described in
:doc:`configurator`.

To see the Encoder in action, using output from the Simple Producer and the
'direct' carriage mechanism, run ``ebu-run
--admin.conf=ebu_tt_live/examples/config/sproducer_ebuttd_direct.json``.

IMPORTANT: the Encoder is not a complete EBU-TT Live to EBU-TT-D converter.
Since EBU-TT-D generation was not part of this project, this functionality was
implemented only partially and should not be used as complete reference.
