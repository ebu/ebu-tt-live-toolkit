User input producer
===================

The user input producer is composed of a user interface written in javascript, the user interface is defined in the file `ebu_tt_live/ui/user_input_producer/user_input_producer.html`. It works with Javascript, JQuery_ and nunjucks_.

Demo
----

To test the user input producer, setup the environment as indicated in the ``README.md`` file at the root of the project. Then launch a node that can listen for /publish requests - for example ``ebu-run --admin.conf ebu_tt_live/examples/config/user_input_producer_consumer.json`` will run the simplest user-input-consumer script listening for a connection on the local host port 9001. Then open the ``ebu_tt_live/ui/user_input_producer/user_input_producer.html`` file in your browser.

If you have no configured sequences or you need to create a new one, click "Create a new sequence", enter the sequence number, what time base and clock mode you want the documents in the sequence to have and click Validate. Assuming all is well you can now use this sequence.

Ensure that the correct URL is present and select the sequence you wish to connect to. The default of ``ws://127.0.0.1:9001`` works with the above simple consumer script configuration. Click Connect to establish the connection - you should see "Connected to websocket server" appear if you have successfully connected.

If for any reason the connection should be closed the text "Connection to websocket server closed." appears next to the Connect button.

There are three ways to trigger when each document will be sent:
    * `on enter, space and escape` will issue a new document each time you click the "Now!" button or every time you type a space or enter or escape in the subtitle text area.
    * `on scheduled time` displays an input box and a "Schedule" button. You have two options, using a "local" clock, which is the time of your computer or using a "media" clock, which is a clock starting at `00:00:00.0` when you click on "Synchronize" button. Times have to be entered using `hh:mm:ss` format in the "Scheduled time" input. When you click on "Schedule" the current document state is set to be sent at the given time. You can now change any field to schedule a new document without waiting.
    * `asynchronously` will send a new document every `x` seconds, taking your modifications on-the-go.

You can configure the maximum number of lines to allow in the subtitle text area by varying the value in the Maximum lines input area. While typing in the subtitle text box pressing Enter will remove lines so that the next document sent does not exceed the Maximum lines setting. Pressing Escape will clear the text area.

Now you are ready to type subtitle text in the `Subtitle text` box. Each time a new document is sent and received it should be logged by the running consumer script.

.. warning:: Note that the simple configuration above creates a simple consumer that handles the first provided sequence identifier. If the connection is disconnected and a new one made with a different sequence identifier it will reject all documents and close the connection. The workaround to this is to restart the consumer and reconnect.

Handover Manager
----------------

To see the UIP in action with the Handover Manager node, using the Websocket transport mechanism, follow these steps:

* Start the Handover Manager: ``ebu-run --admin.conf=ebu_tt_live/examples/config/user_input_producer_handover.json``

* Create two (or more) instances of the User Input Producer by opening ``ebu_tt_live/ui/user_input_producer/user_input_producer.html`` in multiple browser tabs/windows.

* In each instance of the UIP, create a sequence with a different sequence identifier but with identical authors group identifier. If you use the default configuration, this is "TestGroup1".

* Select the sequence you created and connect. The default configuration publishes to ``ws://127.0.0.1:9001``.

* In the Result host panel, connect to the result host - the default configuration subscribes to ``ws://127.0.0.1:9001``. Enter the Handover Manager's output sequence identifier - the default is "HandoverSequence1".

* Enter a positive number in the 'Authors group control token' field.

* Enter subtitle text and send the document.

* The UIP publishing the sequence currently selected by the Handover Manager will display an "On air" flag. This is derived from the ``ebuttm:authorsGroupSelectedSequenceIdentifier`` metadata.

* The output from the handover node will appear in the "Received documents" panel. Click a row to reveal the document or message.

* Non-selected sequences can "take control" by sending a document with a higher control token value than the most recently output document from the Handover Manager, according to the EBU-TT Part 3 specification. To show this, enter a higher number in the Control Token field before sending a document.

You can also send messages (not documents) to all subscribers by entering text in the Control Request field.

.. note:: More demo scenario examples :

    * Run ``ebu-run --admin.conf ebu_tt_live/examples/config/user_input_producer_dist_consumers.json``. This configuration runs a distributor node and two consumers, one for TestSequence1 and the other for TestSequence2. Open the ``ui/user_input_producer/user_input_producer.html`` page and create or select TestSequence1, and connect it to the distributor node via websocket (click "connect" button). When you send a document the consumer will log the new document. Open another user input web page and connect it with TestSequence2. The second consumer receives this document. Now documents can be sent by both web pages simultaneously and will be routed to the correct consumer by the Distributor node.

.. note:: Demo scenario examples that need some more work :

     * Open in a separate window the `test.html` page at the root of the project, connect on this page too.

     * From the user input producer page create a new sequence, on the `test.html` window subscribe to the same sequence. Send documents from the user input producer page. View those pages being validated in the user input forwarder process output. Finally, view the documents arriving on the test.html page. You can even do this with 1x user input forwarder and `n` sequences, generated by `n` user input producer pages and viewed by `m` `test.html` pages.

    * Run `ebu-user-input-forwarder --folder-export output`, this will write all the files you send from the user input producer interface (`ui/user_input_producer/user_input_producer.html`) to the output folder. Create a sequence `testSeq` for example and send one document, in a new terminal run `ebu-simple-consumer -m output/manifest_testSeq.txt -f`. You should see the documents you send from the user input producer interface being validated by the `ebu-user-input-forwarder` process output and then displayed by the `ebu-simple-consumer` script.

You can also try documents being generated on demand, at scheduled times or asynchronously by using the sending modes presented above.

.. _JQuery: https://jquery.com/
.. _nunjucks: https://mozilla.github.io/nunjucks/
