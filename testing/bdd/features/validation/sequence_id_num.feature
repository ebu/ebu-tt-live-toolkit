@validation @syntax @sequence @xsd
Feature: Sequence ID and Sequence Number
  Both are mandatory parameters and the sequence number has to be a number (no letters)

  # SPEC-CONFORMANCE: R6 R7 R34 R35 R36
  Scenario: Invalid Sequence head attributes
    Given an xml file <xml_file>
    When it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    Then document is invalid

    Examples:
    | xml_file            | seq_id   | seq_n |
    | sequence_id_num.xml |          | 5     |
    | sequence_id_num.xml | testSeq1 | a     |
    | sequence_id_num.xml | testSeq1 | -5    |
    | sequence_id_num.xml | testSeq1 |       |
    | sequence_id_num.xml |          |       |

  # SPEC-CONFORMANCE: R6 R7 R34 R35 R36
  Scenario: Valid Sequence head attributes
    Given an xml file <xml_file>
    When it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    Then document is valid

    Examples:
    | xml_file            | seq_id   | seq_n     |
    | sequence_id_num.xml | testSeq1 | 5         |
    | sequence_id_num.xml | a        | 10        |
    | sequence_id_num.xml | testSeq1 | 999999999 |

