@validation @syntax @sequence @xsd
Feature: Sequence ID and Sequence Number
  Both are mandatory parameters and the sequence number has to be a number (no letters).
  Moreover two documents with the same sequence identifier shall have different sequence numbers.

  Examples:
  | xml_file            |
  | sequence_id_num.xml |

  # SPEC-CONFORMANCE: R6 R7 R34 R35 R36
  Scenario: Invalid Sequence head attributes
    Given an xml file <xml_file>
    When it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    Then document is invalid

    Examples:
    | seq_id   | seq_n |
    |          | 5     |
    | testSeq1 | a     |
    | testSeq1 | -5    |
    | testSeq1 |       |
    |          |       |

  # SPEC-CONFORMANCE: R6 R7 R34 R35 R36
  Scenario: Valid Sequence head attributes
    Given an xml file <xml_file>
    When it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    Then document is valid

    Examples:
    | seq_id   | seq_n     |
    | testSeq1 | 5         |
    | a        | 10        |
    | testSeq1 | 999999999 |


  # SPEC-CONFORMANCE: R8 R37
  Scenario: Invalid sequence number for documents in the same sequence
    Given a test sequence
    And an xml file <xml_file>
    When it has sequence number <doc1_seqnum>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequence number <doc2_seqnum>
    Then adding doc2 to the sequence results in an error

    Examples:
    | doc1_seqnum | doc2_seqnum |
    | 1           | 1           |
    | 30          | 30          |


  # SPEC-CONFORMANCE: R8 R37
  Scenario: Valid sequence number for documents in the same sequence
    Given a test sequence
    And an xml file <xml_file>
    When it has sequence number <doc1_seqnum>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequence number <doc2_seqnum>
    Then adding doc2 to the sequence does not raise any error

    Examples:
    | doc1_seqnum | doc2_seqnum |
    | 1           | 2           |
    | 30          | 25          |
