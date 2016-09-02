@validation @syntax @metadata
Feature: Document metadata elements order
  Order of metadata elements (if present) in ebuttm:documentMetadata is: ebuttm:originalSourceServiceIdentifier, 
  ebuttm:intendedDestinationServiceIdentifier, ebuttm:documentFacet, ebuttm:trace

  Examples:
  | xml_file                            |
  | documentMetadata_elements_order.xml |

  # SPEC-CONFORMANCE: R38 R39
  Scenario: Valid documentMetadata elements order
    Given an xml file <xml_file>
    When it has documentMetadata 1 <document_metadata_1>
    And it has documentMetadata 2 <document_metadata_2>
    And it has documentMetadata 3 <document_metadata_3>
    And it has documentMetadata 4 <document_metadata_4>
    Then document is valid

    Examples:
    | document_metadata_1                  | document_metadata_2                  | document_metadata_3 | document_metadata_4 |
    | originalSourceServiceIdentifier      | intendedDestinationServiceIdentifier | documentFacet       | trace               |
    | intendedDestinationServiceIdentifier | documentFacet                        | trace               |                     |
    | documentFacet                        | trace                                |                     |                     |
    | trace                                |                                      |                     |                     |
    | documentIdentifier                   | trace                                |                     |                     |


  # SPEC-CONFORMANCE: R38 R39
  Scenario: Invalid documentMetadata elements order
    Given an xml file <xml_file>
    When it has documentMetadata 1 <document_metadata_1>
    And it has documentMetadata 2 <document_metadata_2>
    And it has documentMetadata 3 <document_metadata_3>
    And it has documentMetadata 4 <document_metadata_4>
    Then document is invalid

    Examples:
    | document_metadata_1                  | document_metadata_2                  | document_metadata_3                  | document_metadata_4             |
    | intendedDestinationServiceIdentifier | originalSourceServiceIdentifier      | documentFacet                        | trace                           |
    | originalSourceServiceIdentifier      | intendedDestinationServiceIdentifier | trace                                | documentFacet                   |
    | originalSourceServiceIdentifier      | documentFacet                        | intendedDestinationServiceIdentifier | trace                           |
    | trace                                | intededDestinationServiceIdentifier  | documentFacet                        | originalSourceServiceIdentifier |
    | originalSourceServiceIdentifier      | documentIdentifier                   |                                      |                                 |
