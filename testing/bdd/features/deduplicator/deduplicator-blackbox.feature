Feature: Deduplicator removes duplicated style and region elements
#  Background:
#    Given a new instance of the deduplicator
#  Examples:
#  | xml_file      |
#  | test_file.xml |

  #Everything goes right
  Scenario: Removes duplicated styles and regions
     Given an xml file <xml_file>
     And a deduplicator node
     When the document is processed
     Then the output document has <style_out_num> styles
     And it has <region_out_num> regions
     And the document is valid

      Examples:
        | xml_file                                                                                      | style_out_num | region_out_num |
        | deduplicator_templates/documentNoStylesNoRegions.xml                                          | 0             | 0              |
        | deduplicator_templates/documentNoStylesOneRegion.xml                                          | 0             | 1              |
        | deduplicator_templates/documentOneStyleNoRegions.xml                                          | 1             | 0              |
        | deduplicator_templates/documentOneStyleOneRegion.xml                                          | 1             | 1              |
        | deduplicator_templates/documentOneStyleOneRegionWithOneStyleAttr.xml                          | 1             | 1              |
        | deduplicator_templates/documentThreeDuplicateStylesThreeDuplicateRegionsAllAttrsSpecified.xml | 1             | 1              |

#  Scenario: Upon receiving more than one file, the deduplicator reads each one sequentially and successfully removes instances of element duplication
#    Given the deduplicator receives more than one file

  #Everything goes wrong
#  Scenario: The deduplicator does nothing if no files are present
#    Given the deduplicator receives no files
#    Then the process terminates
