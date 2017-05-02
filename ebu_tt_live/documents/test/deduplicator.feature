Feature: Deduplicator removes duplication from <style> and <region> elements for one resequenced file

Scenario: The deduplicator accesses a valid resequenced file
  Given the deduplicator has the <filesystem> carriage as input
  And has a manifest_file defined
  Then it looks in the export folder for the manifest_file

Scenario: Upon receiving a resequenced file, the deduplicator goes through and stores the <style> and <region> elements
  Given the deduplicator successfully finds the manifest_file
  And it contains the filename of a resequenced file
  Then it goes through the file

Scenario: The deduplicator compares the elements and assigns the same label to duplicate elements
  Given the deduplicator has successfully read the file
  When it finds duplicate <style> and <region> elements
  Then it assigns a new label to each element, with duplicate ones having the same label

Scenario: The deduplicator creates a new file
  Given the deduplicator has assigned labels to all elements
  And it has the <filesystem> carriage as its output
  Then it creates a new file

Scenario: The deduplicator replaces the <style> and <region> elements, and all references to them with the new labels
  Given the deduplicator has created a new file
  Then it deletes the existing <style> and <region> elements
  And deletes the references to them in the subtitle fields
  Then replaces them with the new unique labels
