Feature: Values of documentRevisionNumber
# This file deals with testing the falsely added default integer value to the revision field, which ends up
# passing validation with an empty value and that is an error. So the fix has to make it work the standard way.

  Examples:
  | xml_file                    |
  |document_revision_number.xml |

  Scenario: documentRevisionNumber valid
    Given an xml file <xml_file>
    When document revision number is <document_revision_number>
    Then document should be valid

    Examples:
    | document_revision_number |
    | 1                        |

    Scenario: documentRevisionNumber invalid
    Given an xml file <xml_file>
    When document revision number is <document_revision_number>
    Then document should be valid

    Examples:
    | document_revision_number |
    | a                        |
    |                          |
