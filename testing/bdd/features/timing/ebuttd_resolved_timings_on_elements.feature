@timing @document @ebuttd_conversion
Feature: Resolving timings on elements

    Examples:
      | xml_file                   |
      | resolved_time_elements.xml |

  Scenario: Timings present on both p and span elements
    Given an xml file <xml_file>
    When  it has p begin time <p_begin>
    And   it has p end time <p_end>
    And   it has span1 begin time <span1_begin>
    And   it has span1 end time <span1_end>
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   span1 resulted begin time is <span1_resulted_begin_time>
    And   span1 resulted end time is <span1_resulted_end_time>
    And   no timings present on p

    Examples:
      | p_begin  | p_end    | span1_begin | span1_end | span1_resulted_begin_time | span1_resulted_end_time |
      | 00:00:05 |          | 00:00:02    | 00:00:08  | 00:00:07                  | 00:00:13                |
      | 00:00:10 | 00:00:15 | 00:00:01    | 00:00:02  | 00:00:11                  | 00:00:12                |
      | 00:00:10 | 00:00:13 |             | 00:00:04  | 00:00:10                  | 00:00:13                |


  Scenario: Timings present on both p and nested span elements
    Given an xml file <xml_file>
    When  it has p begin time <p_begin>
    And   it has p end time <p_end>
    And   it has span1 begin time <span1_begin>
    And   it has span1 end time <span1_end>
    And   it has nestedSpan begin time <nestedSpan_begin>
    And   it has nestedSpan end time <nestedSpan_end>
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   span1 resulted begin time is <span1_resulted_begin_time>
    And   span1 resulted end time is <span1_resulted_end_time>
    And   nestedSpan resulted begin time is <nestedSpan_resulted_begin_time>
    And   nestedSpan resulted end time is <nestedSpan_resulted_end_time>
    And   no timings present on p

    Examples:
      | p_begin  | p_end    | span1_begin | span1_end | nestedSpan_begin | nestedSpan_end | span1_resulted_begin_time | span1_resulted_end_time | nestedSpan_resulted_begin_time | nestedSpan_resulted_end_time |
      | 00:00:05 |          | 00:00:02    | 00:00:08  | 00:00:01         | 00:00:02       | 00:00:07                  | 00:00:13                | 00:00:08                       | 00:00:09                     |
      | 00:00:05 |          | 00:00:02    | 00:00:08  | 00:00:03         | 00:00:05       | 00:00:07                  | 00:00:13                | 00:00:10                       | 00:00:12                     |
      | 00:00:05 |          | 00:00:02    | 00:00:08  | 00:00:03         |                | 00:00:07                  | 00:00:13                | 00:00:10                       | 00:00:13                     |
      | 00:00:05 |          | 00:00:02    | 00:00:08  |                  | 00:00:06       | 00:00:07                  | 00:00:13                | 00:00:07                       | 00:00:13                     |

  Scenario: Timings specified on div, body and p shall be removed
    Given an xml file <xml_file>
    When  it has div begin time <div_begin>
    And   it has div end time <div_end>
    And   it has body begin time <body_begin>
    And   it has body end time <body_end>
    And   it has p begin time <p_begin>
    And   it has p end time <p_end>
    And   it has span1 begin time <span1_begin>
    And   it has span1 end time <span1_end>
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   span1 resulted begin time is <span1_resulted_begin_time>
    And   span1 resulted end time is <span1_resulted_end_time>
    And   no timings present on p
    And   no timings present on div
    And   no timings present on body


    Examples:
      | body_begin | body_end | div_begin | div_end  | p_begin  | p_end    | span1_begin | span1_end | span1_resulted_begin_time | span1_resulted_end_time |
      | 00:01:30   |          | 00:00:01  | 00:00:20 | 00:00:02 | 00:00:13 | 00:00:05    | 00:00:07  | 00:01:38                  | 00:01:40                |
      | 00:01:00   |          | 00:00:02  | 00:00:24 | 00:00:01 | 00:00:12 | 00:00:01    | 00:00:04  | 00:01:04                  | 00:01:07                |
      | 00:01:00   | 00:01:40 | 00:00:02  |          |          |          | 00:00:08    | 00:00:20  | 00:01:10                  | 00:01:22                |

  Scenario: Timings specified on div, body shall be removed
    Given an xml file <xml_file>
    When  it has div begin time <div_begin>
    And   it has div end time <div_end>
    And   it has body begin time <body_begin>
    And   it has body end time <body_end>
    And   it has p begin time <p_begin>
    And   it has p end time <p_end>
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  p resulted begin time is <p_resulted_begin_time>
    And   p resulted end time is <p_resulted_end_time>
    And   no timings present on div
    And   no timings present on body

    Examples:
      | body_begin | body_end | div_begin | div_end  | p_begin  | p_end    | p_resulted_begin_time | p_resulted_end_time |
      | 00:01:10   |          | 00:00:01  | 00:00:04 | 00:00:02 | 00:00:03 | 00:01:13              | 00:01:14            |
      | 00:01:00   |          | 00:00:02  | 00:00:08 | 00:00:01 | 00:00:03 | 00:01:03              | 00:01:05            |
      | 00:01:00   |          |           |          | 00:00:00 |          | 00:01:00              | None                |
      |            |          | 00:01:00  |          | 00:00:00 |          | 00:01:00              | None                |
      |            |          |           |          | 00:01:00 |          | 00:01:00              | None                |
      