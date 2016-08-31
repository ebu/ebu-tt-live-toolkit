Filesystem Carriage Mechanism
=============================

The filesystem carriage mechanism writes produced documents to the filesystem and consumes documents from the filesystem. Along with the documents, it writes a manifest file named according to the format `manifest_<sequence identifier>.txt`. Documents are named following the format `<sequence identifier>_<sequence number>.xml`. 

Each time a document is written to the file system, a line using the following format is appended to the manifest file:

`availability_time,path_to_xml_file`

For example:

`09:20:31.279,TestSequence1_474.xml`

The format is `hh:mm:ss.fff,path` where `fff` represents milliseconds digits.

The manifest file gives the availability time for each document along with the path to the corresponding document. The timeline used for the availability times is the same as the one used in the documents, indeed the carriage implementation uses the same clock (or time reference) as the node that produces the documents. The writing order and thus the reading order is from top to bottom.
