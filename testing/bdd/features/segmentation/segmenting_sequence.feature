@segmentation @sequence

Feature: Segmentation of document sequence

  Examples:
  | xml_file               | sequence_identifier | time_base | body_dur | span1_begin | span1_end | span2_begin | span2_end |
  | segmentation_short.xml | test                | media     | 00:00:05 | 00:00:01    | 00:00:02  | 00:00:03    | 00:00:04  |

  Scenario: Get parts of sequence
    Given an xml file <xml_file>
    And a sequence <sequence_identifier> with timeBase <time_base>
    When we create a new document with <body_dur> <span1_begin> <span2_begin> <span1_end> <span2_end>
    And body begins at <body1_begin>
    And document added to the sequence
    And we create a new document with <body_dur> <span1_begin> <span2_begin> <span1_end> <span2_end>
    And body begins at <body2_begin>
    And document added to the sequence
    And we create a new document with <body_dur> <span1_begin> <span2_begin> <span1_end> <span2_end>
    And body begins at <body3_begin>
    And document added to the sequence
    And the sequence is segmented from <range_from> to <range_to>
    Then the fragment contains body with computed times from <frag_body_begin> to <frag_body_end>
    And the fragment only contains styles <frag_styles>
    And the fragment only contains regions <frag_regions>


    Examples:
    | body1_begin | body2_begin | body3_begin | range_from | range_to | frag_body_begin | frag_body_end | frag_styles                                                                                                         | frag_regions                             |
    | 00:00:00    | 00:00:06    | 00:00:12    | 00:00:00   | 00:00:17 | 00:00:01        | 00:00:16      | SEQ1.style1, SEQ1.style2, SEQ1.style3, SEQ2.style1, SEQ2.style2, SEQ2.style3, SEQ3.style1, SEQ3.style2, SEQ3.style3 | SEQ1.region1, SEQ2.region1, SEQ3.region1 |
    | 00:00:00    | 00:00:06    | 00:00:12    | 00:00:00   | 00:00:12 | 00:00:01        | 00:00:10      | SEQ1.style1, SEQ1.style2, SEQ1.style3, SEQ2.style1, SEQ2.style2, SEQ2.style3                                        | SEQ1.region1, SEQ2.region1               |
    | 00:00:00    | 00:00:06    | 00:00:12    | 00:00:00   | 00:00:09 | 00:00:01        | 00:00:08      | SEQ1.style1, SEQ1.style2, SEQ1.style3, SEQ2.style1, SEQ2.style2, SEQ2.style3                                        | SEQ1.region1, SEQ2.region1               |
    | 00:00:00    | 00:00:06    | 00:00:12    | 00:00:05   | 00:00:09 | 00:00:07        | 00:00:08      | SEQ2.style1, SEQ2.style2, SEQ2.style3                                                                               | SEQ2.region1                             |
    | 00:00:00    | 00:00:06    | 00:00:12    | 00:00:02   | 00:00:09 | 00:00:03        | 00:00:08      | SEQ1.style1, SEQ1.style2, SEQ1.style3, SEQ2.style1, SEQ2.style2, SEQ2.style3                                        | SEQ1.region1, SEQ2.region1               |
    | 00:00:00    | 00:00:06    | 00:00:12    | 00:00:05   | 00:00:07 | 00:00:05        | 00:00:07      | SEQ2.style2                                                                                                         |                                          |