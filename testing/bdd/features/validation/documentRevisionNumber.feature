@validation @syntax
Feature: Values of documentRevisionNumber
# This file deals with testing the falsely added default integer value to the revision field, which ends up
# passing validation with an empty value and that is an error. So the fix has to make it work the standard way.

  Examples:
  | xml_file                    |
  |document_revision_number.xml |

  Scenario: documentRevisionNumber valid
    Given an xml file <xml_file>
    When document revision number is <document_revision_number>
    Then document is valid

    Examples:
    | document_revision_number |
    | 1                        |

    Scenario: documentRevisionNumber invalid
    Given an xml file <xml_file>
    When document revision number is <document_revision_number>
    Then document is invalid

    Examples:
    | document_revision_number |
    |                          |  # This is a tricky case that passes validation because of PyXB https://github.com/pabigot/pyxb/issues/71
    | -1                       |
    | a                        |
    | 12s                      |
    | 1 3                      |
    | ,                        |
    | 1,2                      |
    | 1.2                      |
