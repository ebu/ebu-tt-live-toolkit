@segmentation @document

Feature: Segmentation of single document into pieces 1

  Examples:
  | xml_file         | sequence_identifier | sequence_number | body_begin | body_end | span1_begin | span1_end | span2_begin | span2_end | span3_begin | span3_end |
  | segmentation.xml | test                | 1               | 00:00:00   | 00:00:10 | 00:00:01    | 00:00:02  | 00:00:03    | 00:00:04  | 00:00:05    | 00:00:06  |

  Scenario: Get parts of document
    Given an xml file <xml_file>
    When it has sequenceIdentifier <sequence_identifier>
    And it has sequenceNumber <sequence_number>
    And it has body from <body_begin> to <body_end>
    And it has span1 from <span1_begin> to <span1_end>
    And it has span2 from <span2_begin> to <span2_end>
    And it has span3 from <span3_begin> to <span3_end>
    And the range from <range_from> to <range_to> is requested
    Then the fragment contains body with computed times from <frag_body_begin> to <frag_body_end>
    And the fragment contains span1 with computed times from <frag_span1_begin> to <frag_span1_end>
    And the fragment contains span2 with computed times from <frag_span2_begin> to <frag_span2_end>
    And the fragment contains span3 with computed times from <frag_span3_begin> to <frag_span3_end>
    And the fragment only contains styles <frag_styles>
    And the fragment only contains regions <frag_regions>

    Examples:
    | range_from | range_to  | frag_body_begin | frag_body_end | frag_span1_begin | frag_span1_end | frag_span2_begin | frag_span2_end | frag_span3_begin | frag_span3_end | frag_styles                    | frag_regions |
    | 00:00:00   | 00:00:10  | 00:00:01        | 00:00:06      | 00:00:01         | 00:00:02       | 00:00:03         | 00:00:04       | 00:00:05         | 00:00:06       | style1, style2, style3, style4 | region1      |
    | 00:00:00   | 00:00:06  | 00:00:01        | 00:00:06      | 00:00:01         | 00:00:02       | 00:00:03         | 00:00:04       | 00:00:05         | 00:00:06       | style1, style2, style3, style4 | region1      |
    | 00:00:00   | 00:00:05.5| 00:00:01        | 00:00:05.5    | 00:00:01         | 00:00:02       | 00:00:03         | 00:00:04       | 00:00:05         | 00:00:05.5     | style1, style2, style3, style4 | region1      |
    | 00:00:01   | 00:00:10  | 00:00:01        | 00:00:06      | 00:00:01         | 00:00:02       | 00:00:03         | 00:00:04       | 00:00:05         | 00:00:06       | style1, style2, style3, style4 | region1      |
    | 00:00:01.5 | 00:00:10  | 00:00:01.5      | 00:00:06      | 00:00:01.5       | 00:00:02       | 00:00:03         | 00:00:04       | 00:00:05         | 00:00:06       | style1, style2, style3, style4 | region1      |
    | 00:00:02   | 00:00:10  | 00:00:03        | 00:00:06      | deleted          |                | 00:00:03         | 00:00:04       | 00:00:05         | 00:00:06       | style1, style2, style3         | region1      |
    | 00:00:06   | 00:00:10  | 00:00:06        | 00:00:10      | deleted          |                | deleted          |                | deleted          |                | style2                         |              |
    | 00:00:04   | 00:00:05  | 00:00:04        | 00:00:05      | deleted          |                | deleted          |                | deleted          |                | style2                         |              |

