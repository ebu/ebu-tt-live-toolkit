Nodes and Carriage Mechanisms
=============================

   The following piece should present the decisions behind the Node architecture and the carriage mechanism pluggability.

   .. uml:: nodes_and_carriages_comp.puml
      :caption: Processing node and Carriage mechanism components

Processing Nodes
----------------

   The processing nodes are the key components of this package and facilitate several different use-cases laid out
   in the Node conformance section of EBU-3370. A node can be a producer or a consumer or both. This requirement
   is fulfilled by the class structure depicted below.

   .. uml:: inode.puml
      :caption: Processing node classes

Carriage mechanisms
-------------------

   The carriage mechanisms are divided into 2 distinct kinds: producer and consumer carriages:

   Producers serve the purpose of sending/serialising a document once a processing node
   has finished processing them and push them via their domain forward.

   Consumers on the other hand receive a (probably serialised) document from their own domain and
   their job is to make sure the document is picked up (possibly parsed and validated) and given
   to the consumer processing node that the carriage mechanism object is registered to.

   The class hierarchy providing the necessary steps looks the following way:

   .. uml:: icarriage.puml
      :caption: Carriage mechanism classes

   .. toctree::
      filesystem_carriage_mechanism
      websocket_carriage_mechanism
      direct_carriage_mechanism
