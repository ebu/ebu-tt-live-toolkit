Timing resolution and consumer logic
====================================

EBU-TT part 3 deals with sequences of documents and uses those combined to create a single timeline/sequence where
document contents(ISD) begin and end events are kept. Resolving this takes resolving the document timings first.
After each document's internal timing relationships have been worked out the document is getting inserted into the
timeline where possible collisions are detected and resolved with the possible discarding of documents in the process.

The document timing resolution logic is built using the validation framework and mostly is in
