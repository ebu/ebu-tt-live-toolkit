Feature: Sequence ID and Sequence Number
    Both are mandatory parameters and the sequence number has to be a number (no letters)

    Scenario: Invalid Sequence head attributes
        Given an xml file <xml_file>
        And it has sequence identifier <seq_id>
        And it has sequence number <seq_n>
        Then document is invalid

        Examples:
        | xml_file            | seq_id   | seq_n |
        | sequence_id_num.xml |          | 5     |
        | sequence_id_num.xml | testSeq1 | a     |
        | sequence_id_num.xml | testSeq1 | -5    |
        | sequence_id_num.xml | testSeq1 |       |
        | sequence_id_num.xml |          |       |

    Scenario: Valid Sequence head attributes
        Given an xml file <xml_file>
        And it has sequence identifier <seq_id>
        And it has sequence number <seq_n>
        Then document is valid

        Examples:
        | xml_file            | seq_id   | seq_n     |
        | sequence_id_num.xml | testSeq1 | 5         |
        | sequence_id_num.xml | a        | *?Empty?* |
        | sequence_id_num.xml | testSeq1 | 999999999 |

