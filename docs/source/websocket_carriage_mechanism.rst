WebSocket Carriage Mechanism
=============================

The WebSocket carriage mechanism writes produced documents to WebSocket connections and consumes documents from WebSocket connections. This is conformant to the EBU-TT Live WebSocket Carriage Mechanism specification, using the URL form: ::

	ws://[host]:[port]:[sequenceId]/[publish | subscribe]

There are two ways to make a connection between node A and node B where documents of sequence "Sequence1" flow from A to B.

1. Node A makes a /publish connection, for example: ::

	ws://1.2.3.4:9000/Sequence1/publish

2. Node B makes a /subscribe connection, for example : ::

	ws://1.2.3.4/9001/Sequence1/subscribe

If the sequence identifier contains a character that is reserved for use in URLs then it must be percent encoded exactly once before inserting into the URL. For example a sequence id "abc/def" becomes "abc%2Fdef" before inserting into the URL.

Error handling
--------------

The expected documents are those that have the correct sequence number and flow from the emitter to the receiver. As per the specification, any unexpected data will cause the connection to be closed. These include:

* Any data received by the emitter, since this reverse flow of data is unexpected.
* Any document with a non-matching sequence identifier
* Any data that is not a valid document
