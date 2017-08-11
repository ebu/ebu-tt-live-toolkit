Feature: Deduplicator removes duplicated style and region elements
#  Background:
#    Given a new instance of the deduplicator
#  Examples:
#  | xml_file      |
#  | test_file.xml |

  #Tests single document inputs
  Scenario: Removes duplicated styles and regions
     Given an xml file <xml_file>
     And the document is generated
     And a deduplicator node
     When the document is processed
     Then the output document has <style_out_num> styles
     And it has <region_out_num> regions
     And document is valid

      Examples:
        | xml_file                                                                              | style_out_num | region_out_num |
        | deduplicator_templates/NoStylesNoRegions.xml                                          | 0             | 0              |
        | deduplicator_templates/NoStylesOneRegion.xml                                          | 0             | 1              |
        | deduplicator_templates/OneStyleNoRegions.xml                                          | 1             | 0              |
        | deduplicator_templates/OneStyleOneRegion.xml                                          | 1             | 1              |
        | deduplicator_templates/OneStyleOneRegionWithOneStyleAttr.xml                          | 1             | 1              |
        | deduplicator_templates/ThreeDuplicateStylesThreeDuplicateRegionsAllAttrsSpecified.xml | 1             | 1              |
        | deduplicator_templates/1Sty1Reg4DupAtts.xml                                           | 1             | 1              |
        | deduplicator_templates/3DupSty3DupRegRefs.xml                                         | 1             | 1              |
        | deduplicator_templates/6Sty3Dup6Reg3DupForeignNamespace.xml                           | 4             | 4              |
        | deduplicator_templates/NoDupStyNoDupReg.xml                                           | 6             | 3              |
        | deduplicator_templates/TwoDuplicateStylesNoRegions.xml                                | 1             | 0              |
        | deduplicator_templates/NoStylesTwoDuplicateRegions.xml                                | 0             | 1              |
        | deduplicator_templates/4Sty2Dup5Reg2Dup2SimilarForeignNamespacesEach.xml              | 3             | 4              |

  #Test more than one document input
  Scenario: Successfully removes styles and regions of more than one document
    Given a first xml file <xml_file_1>
    And the first document is generated
    And a deduplicator node
    When the first document is processed
    Then the first output document has <style_out_num_1> styles
    And the first output document has <region_out_num_1> regions
    And the first document is valid
    Then a second xml file <xml_file_2>
    And the second document is generated
    And the second document is processed
    Then the second output document has <style_out_num_2> styles
    And the second output document has <region_out_num_2> regions
    And the second document is valid

      Examples:
        | xml_file_1                                 | style_out_num_1 | region_out_num_1 | xml_file_2                                 | style_out_num_2 | region_out_num_2 |
        | deduplicator_templates/ReSequenced1_12.xml | 5               | 2                | deduplicator_templates/ReSequenced1_13.xml | 1               | 1                |


#  Scenario: Upon receiving more than one file, the deduplicator reads each one sequentially and successfully removes instances of element duplication
#    Given the deduplicator receives more than one file

  #Everything goes wrong
#  Scenario: The deduplicator does nothing if no files are present
#    Given the deduplicator receives no files
#    Then the process terminates

#Everything goes right
#  Scenario: Replace references for merged styles and regions
#     Given an xml file <xml_file>
#     And a deduplicator node
#     When the document is processed
#     Then all style attributes contain a single style reference
#     And all style attributes contain the same style reference
#     And all region attributes contain the same region reference
#     And all region attributes contain the same style reference
#     And the document is valid

#      Examples:
#        | xml_file                                      |
#        | deduplicator_templates/3DupSty3DupRegRefs.xml |
#        | deduplicator_templates/1Sty1Reg4DupAtts.xml   |
