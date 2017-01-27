Direct Carriage Mechanism
=============================

The direct carriage mechanism copies documents in memory via a named "pipe" [#]_ from one node to another node. When configuring nodes to use the direct carriage mechanism the node emitting a document must specify the same pipe name as the node receiving that document.

This carriage mechanism facilitates efficient chaining of nodes that perform sequential processing to the same content without having to use the network stack or local storage, however it requires the nodes to be hosted in the same process running on the same machine.

.. rubric:: Footnotes

.. [#] This is similar in concept to a UNIX pipe but completely unrelated in the implementation.