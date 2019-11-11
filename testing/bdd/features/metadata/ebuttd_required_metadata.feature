@metadata @document @ebuttd_conversion 
Feature: Converted EBUTTD file contains required metadata elements

  Scenario: It adds two conformsToStandard elements to the EBU-TT-D metadata
    Given an xml file <xml_file>
    When the document is generated
    And the EBU-TT-Live document is denested
    And the EBU-TT-Live document is converted to EBU-TT-D
    Then EBUTTD document is valid
    And the EBUTTD document contains a documentMetadata element <element_name> with value <element_value>

    Examples:
      | xml_file                    | element_name       | element_value                                |
      | complete_document_media.xml | conformsToStandard | http://www.w3.org/ns/ttml/profile/imsc1/text |
      | complete_document_media.xml | conformsToStandard | urn:ebu:tt:distribution:2018-04              |
