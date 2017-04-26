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
    | originalSourceServiceIdentifier      | intendedDestinationServiceIdentifier | documentFacet       | appliedProcessing   |
    | intendedDestinationServiceIdentifier | documentFacet                        | appliedProcessing   |                     |
    | documentFacet                        | appliedProcessing                    |                     |                     |
    | appliedProcessing                    |                                      |                     |                     |
    | documentIdentifier                   | appliedProcessing                    |                     |                     |


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
    | intendedDestinationServiceIdentifier | originalSourceServiceIdentifier      | documentFacet                        | appliedProcessing               |
    | originalSourceServiceIdentifier      | intendedDestinationServiceIdentifier | appliedProcessing                    | documentFacet                   |
    | originalSourceServiceIdentifier      | documentFacet                        | intendedDestinationServiceIdentifier | appliedProcessing               |
    | appliedProcessing                    | intededDestinationServiceIdentifier  | documentFacet                        | originalSourceServiceIdentifier |
    | originalSourceServiceIdentifier      | documentIdentifier                   |                                      |                                 |
