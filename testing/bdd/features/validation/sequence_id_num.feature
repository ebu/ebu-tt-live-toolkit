@validation @syntax @sequence @xsd
Feature: Sequence ID and Sequence Number
  Both are mandatory parameters and the sequence number has to be a number (no letters)

  # SPEC-CONFORMANCE: R6 R7 R34 R35 R36 R124
  Scenario Outline: Invalid Sequence head attributes
    Given an xml file "sequence_id_num.xml"
    When it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    Then document is invalid

    Examples:
    | seq_id    | seq_n |
    |           | 5     |
    | testSeq1  | a     |
    | testSeq1  | -5    |
    | testSeq1  |       |
    |           |       |
    | *?Empty?* |       |
    | *?Empty?* | 5     |

  # SPEC-CONFORMANCE: R6 R7 R34 R35 R36
  Scenario Outline: Valid Sequence head attributes
    Given an xml file "sequence_id_num.xml"
    When it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    Then document is valid

    Examples:
    | seq_id   | seq_n     |
    | testSeq1 | 5         |
    | a        | 10        |
    | testSeq1 | 999999999 |
