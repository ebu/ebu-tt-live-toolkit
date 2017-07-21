Feature: Deduplicator removes duplicated style and region elements

#  Examples:
#  | xml_file      |
#  | test_file.xml |

  #Everything goes right
  Scenario: The deduplicator emits a document that has instances of duplicated <style> and <region> elements removed
     Given an <xml_file>
     When the deduplicator node processes the document
     Then the output document has <style_out_num> styles
     And it has <region_out_num> regions
     And the document is valid

      Examples:
        | xml_file | style_out_num | region_out_num |

#  Scenario: Upon receiving more than one file, the deduplicator reads each one sequentially and successfully removes instances of element duplication
#    Given the deduplicator receives more than one file

  #Everything goes wrong
  Scenario: The deduplicator does nothing if no files are present
    Given the deduplicator receives no files
    Then the process terminates
