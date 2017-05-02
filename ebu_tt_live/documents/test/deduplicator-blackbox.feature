Feature: Deduplicator removes duplicated style and region elements

#TrueEnd
Scenario: The deduplicator successfully removes instances of element duplication from a file
  When the deduplicator receives a file
  Then it replaces instances of duplicated style and region elements with new labels
  And outputs a new file with a new sequenceIdentifier and sequenceNumber

Scenario: Upon receiving a set of files, the deduplicator

#BadEnd
Scenario: The deduplicator does nothing if no files are present
  When the deduplicator receives no files
  Then the process terminates
