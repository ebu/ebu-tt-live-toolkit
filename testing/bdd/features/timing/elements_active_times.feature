@timing @resolution @element
Feature: Computed element active begin and end times
  # Assuming that parent end = min(explicit end, begin+dur) where dur may exist, i.e. for body element.


  # Given a parent element with one child element, the computed active parent and child begin and active parent end times are valid:
  Examples:
  | xml_file                           | sequence_identifier | sequence_number | time_base |
  | elements_active_time_semantics.xml | testSeq             | 1               | media     |


  Scenario: Parent with one child element
    Given an xml file <xml_file>
    When it has sequenceIdentifier <sequence_identifier>
    And it has sequenceNumber <sequence_number>
    And it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    And the document is generated
    Then body active begin time is <body_active_begin>
    And body active end time is <body_active_end>
    And div active begin time is <div_active_begin>
    And div active end time is <div_active_end>

    Examples:
    | body_begin | body_end | div_begin | div_end  | body_active_begin | body_active_end | div_active_begin | div_active_end |
    |            |          |           |          | 00:00:00          | undefined       | 00:00:00         | undefined      |
    | 00:01:00   |          |           |          | 00:01:00          | undefined       | 00:01:00         | undefined      |
    |            | 00:01:30 |           |          | 00:00:00          | 00:01:30        | 00:00:00         | 00:01:30       |
    | 00:01:00   | 00:01:30 |           |          | 00:01:00          | 00:01:30        | 00:01:00         | 00:01:30       |
    |            |          | 00:01:08  |          | 00:01:08          | undefined       | 00:01:08         | undefined      |
    | 00:01:00   |          | 00:00:08  |          | 00:01:00          | undefined       | 00:01:08         | undefined      |
    |            | 00:01:30 | 00:01:08  |          | 00:01:08          | 00:01:30        | 00:01:08         | 00:01:30       |
    | 00:01:00   | 00:01:30 | 00:00:08  |          | 00:01:00          | 00:01:30        | 00:01:08         | 00:01:30       |
    |            |          | 00:01:08  | 00:01:20 | 00:01:08          | 00:01:20        | 00:01:08         | 00:01:20       |
    | 00:01:00   |          | 00:00:08  | 00:00:20 | 00:01:00          | 00:01:20        | 00:01:08         | 00:01:20       |
    |            | 00:01:30 | 00:01:08  | 00:01:20 | 00:01:08          | 00:01:30        | 00:01:08         | 00:01:20       |
    | 00:01:00   | 00:01:30 | 00:00:08  | 00:00:20 | 00:01:00          | 00:01:30        | 00:01:08         | 00:01:20       |
    |            |          |           | 00:01:20 | 00:00:00          | 00:01:20        | 00:00:00         | 00:01:20       |
    | 00:01:00   |          |           | 00:00:20 | 00:01:00          | 00:01:20        | 00:01:00         | 00:01:20       |
    |            | 00:01:30 |           | 00:01:20 | 00:00:00          | 00:01:30        | 00:00:00         | 00:01:20       |
    | 00:01:00   | 00:01:30 |           | 00:00:20 | 00:01:00          | 00:01:30        | 00:01:00         | 00:01:20       |


  # Given a parent element with two child elements, the computed active parent and child begin and active parent end times are valid:
  Scenario: Parent with two child elements
    Given an xml file <xml_file>
    When it has sequenceIdentifier <sequence_identifier>
    And it has sequenceNumber <sequence_number>
    And it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    And it has span1 begin time <span1_begin>
    And it has span1 end time <span1_end>
    And it has span2 begin time <span2_begin>
    And it has span2 end time <span2_end>
    And the document is generated
    Then p active begin time is <p_active_begin>
    And p active end time is <p_active_end>
    And span1 active begin time is <span1_active_begin>
    And span1 active end time is <span1_active_end>
    And span2 active begin time is <span2_active_begin>
    And span2 active end time is <span2_active_end>

    Examples:
    | p_begin  | p_end    | span1_begin | span1_end | span2_begin | span2_end | p_active_begin | p_active_end | span1_active_begin | span1_active_end | span2_active_begin | span2_active_end |
    |          |          |             |           |             |           | 00:00:00       | undefined    | 00:00:00           | undefined        | 00:00:00           | undefined        |
    | 00:01:00 |          |             |           |             |           | 00:01:00       | undefined    | 00:01:00           | undefined        | 00:01:00           | undefined        |
    |          | 00:01:30 |             |           |             |           | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:30         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |           |             |           | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:30         | 00:01:00           | 00:01:30         |
    |          |          | 00:01:08    |           |             |           | 00:00:00       | undefined    | 00:01:08           | undefined        | 00:00:00           | undefined        |
    | 00:01:00 |          | 00:00:08    |           |             |           | 00:01:00       | undefined    | 00:01:08           | undefined        | 00:01:00           | undefined        |
    |          | 00:01:30 | 00:01:08    |           |             |           | 00:00:00       | 00:01:30     | 00:01:08           | 00:01:30         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |           |             |           | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:30         | 00:01:00           | 00:01:30         |
    |          |          | 00:01:08    |  00:01:20 |             |           | 00:00:00       | undefined    | 00:01:08           | 00:01:20         | 00:00:00           | undefined        |
    | 00:01:00 |          | 00:00:08    |  00:00:20 |             |           | 00:01:00       | undefined    | 00:01:08           | 00:01:20         | 00:01:00           | undefined        |
    |          | 00:01:30 | 00:01:08    |  00:01:20 |             |           | 00:00:00       | 00:01:30     | 00:01:08           | 00:01:20         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |  00:00:20 |             |           | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:20         | 00:01:00           | 00:01:30         |
    |          |          |             |  00:01:20 |             |           | 00:00:00       | undefined    | 00:00:00           | 00:01:20         | 00:00:00           | undefined        |
    | 00:01:00 |          |             |  00:00:20 |             |           | 00:01:00       | undefined    | 00:01:00           | 00:01:20         | 00:01:00           | undefined        |
    |          | 00:01:30 |             |  00:01:20 |             |           | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:20         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |  00:00:20 |             |           | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:20         | 00:01:00           | 00:01:30         |
    |          |          |             |           | 00:01:15    |           | 00:00:00       | undefined    | 00:00:00           | undefined        | 00:01:15           | undefined        |
    | 00:01:00 |          |             |           | 00:00:15    |           | 00:01:00       | undefined    | 00:01:00           | undefined        | 00:01:15           | undefined        |
    |          | 00:01:30 |             |           | 00:01:15    |           | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:30         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |           | 00:00:15    |           | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:30         | 00:01:15           | 00:01:30         |
    |          |          | 00:01:08    |           | 00:01:15    |           | 00:01:08       | undefined    | 00:01:08           | undefined        | 00:01:15           | undefined        |
    | 00:01:00 |          | 00:00:08    |           | 00:00:15    |           | 00:01:00       | undefined    | 00:01:08           | undefined        | 00:01:15           | undefined        |
    |          | 00:01:30 | 00:01:08    |           | 00:01:15    |           | 00:01:08       | 00:01:30     | 00:01:08           | 00:01:30         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |           | 00:00:15    |           | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:30         | 00:01:15           | 00:01:30         |
    |          |          | 00:01:08    |  00:01:20 | 00:01:15    |           | 00:01:08       | undefined    | 00:01:08           | 00:01:20         | 00:01:15           | undefined        |
    | 00:01:00 |          | 00:00:08    |  00:00:20 | 00:00:15    |           | 00:01:00       | undefined    | 00:01:08           | 00:01:20         | 00:01:15           | undefined        |
    |          | 00:01:30 | 00:01:08    |  00:01:20 | 00:01:15    |           | 00:01:08       | 00:01:30     | 00:01:08           | 00:01:20         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |  00:00:20 | 00:00:15    |           | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:20         | 00:01:15           | 00:01:30         |
    |          |          |             |  00:01:20 | 00:01:15    |           | 00:00:00       | undefined    | 00:00:00           | 00:01:20         | 00:01:15           | undefined        |
    | 00:01:00 |          |             |  00:00:20 | 00:00:15    |           | 00:01:00       | undefined    | 00:01:00           | 00:01:20         | 00:01:15           | undefined        |
    |          | 00:01:30 |             |  00:01:20 | 00:01:15    |           | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:20         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |  00:00:20 | 00:00:15    |           | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:20         | 00:01:15           | 00:01:30         |
    |          |          |             |           |             | 00:01:35  | 00:00:00       | undefined    | 00:00:00           | undefined        | 00:00:00           | 00:01:35         |
    | 00:01:00 |          |             |           |             | 00:00:35  | 00:01:00       | undefined    | 00:01:00           | undefined        | 00:01:00           | 00:01:35         |
    |          | 00:01:30 |             |           |             | 00:01:35  | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:30         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |           |             | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:30         | 00:01:00           | 00:01:30         |
    |          |          | 00:01:08    |           |             | 00:01:35  | 00:00:00       | undefined    | 00:01:08           | undefined        | 00:00:00           | 00:01:35         |
    | 00:01:00 |          | 00:00:08    |           |             | 00:00:35  | 00:01:00       | undefined    | 00:01:08           | undefined        | 00:01:00           | 00:01:35         |
    |          | 00:01:30 | 00:01:08    |           |             | 00:01:35  | 00:00:00       | 00:01:30     | 00:01:08           | 00:01:30         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |           |             | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:30         | 00:01:00           | 00:01:30         |
    |          |          | 00:01:08    |  00:01:20 |             | 00:01:35  | 00:00:00       | 00:01:35     | 00:01:08           | 00:01:20         | 00:00:00           | 00:01:35         |
    | 00:01:00 |          | 00:00:08    |  00:00:20 |             | 00:00:35  | 00:01:00       | 00:01:35     | 00:01:08           | 00:01:20         | 00:01:00           | 00:01:35         |
    |          | 00:01:30 | 00:01:08    |  00:01:20 |             | 00:01:35  | 00:00:00       | 00:01:30     | 00:01:08           | 00:01:20         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |  00:00:20 |             | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:20         | 00:01:00           | 00:01:30         |
    |          |          |             |  00:01:20 |             | 00:01:35  | 00:00:00       | 00:01:35     | 00:00:00           | 00:01:20         | 00:00:00           | 00:01:35         |
    | 00:01:00 |          |             |  00:00:20 |             | 00:00:35  | 00:01:00       | 00:01:35     | 00:01:00           | 00:01:20         | 00:01:00           | 00:01:35         |
    |          | 00:01:30 |             |  00:01:20 |             | 00:01:35  | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:20         | 00:00:00           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |  00:00:20 |             | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:20         | 00:01:00           | 00:01:30         |
    |          |          |             |           | 00:01:15    | 00:01:35  | 00:00:00       | undefined    | 00:00:00           | undefined        | 00:01:15           | 00:01:35         |
    | 00:01:00 |          |             |           | 00:00:15    | 00:00:35  | 00:01:00       | undefined    | 00:01:00           | undefined        | 00:01:15           | 00:01:35         |
    |          | 00:01:30 |             |           | 00:01:15    | 00:01:35  | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:30         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |           | 00:00:15    | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:30         | 00:01:15           | 00:01:30         |
    |          |          | 00:01:08    |           | 00:01:15    | 00:01:35  | 00:01:08       | undefined    | 00:01:08           | undefined        | 00:01:15           | 00:01:35         |
    | 00:01:00 |          | 00:00:08    |           | 00:00:15    | 00:00:35  | 00:01:00       | undefined    | 00:01:08           | undefined        | 00:01:15           | 00:01:35         |
    |          | 00:01:30 | 00:01:08    |           | 00:01:15    | 00:01:35  | 00:01:08       | 00:01:30     | 00:01:08           | 00:01:30         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |           | 00:00:15    | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:30         | 00:01:15           | 00:01:30         |
    |          |          | 00:01:08    |  00:01:20 | 00:01:15    | 00:01:35  | 00:01:08       | 00:01:35     | 00:01:08           | 00:01:20         | 00:01:15           | 00:01:35         |
    | 00:01:00 |          | 00:00:08    |  00:00:20 | 00:00:15    | 00:00:35  | 00:01:00       | 00:01:35     | 00:01:08           | 00:01:20         | 00:01:15           | 00:01:35         |
    |          | 00:01:30 | 00:01:08    |  00:01:20 | 00:01:15    | 00:01:35  | 00:01:08       | 00:01:30     | 00:01:08           | 00:01:20         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 | 00:00:08    |  00:00:20 | 00:00:15    | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:08           | 00:01:20         | 00:01:15           | 00:01:30         |
    |          |          |             |  00:01:20 | 00:01:15    | 00:01:35  | 00:00:00       | 00:01:35     | 00:00:00           | 00:01:20         | 00:01:15           | 00:01:35         |
    | 00:01:00 |          |             |  00:00:20 | 00:00:15    | 00:00:35  | 00:01:00       | 00:01:35     | 00:01:00           | 00:01:20         | 00:01:15           | 00:01:35         |
    |          | 00:01:30 |             |  00:01:20 | 00:01:15    | 00:01:35  | 00:00:00       | 00:01:30     | 00:00:00           | 00:01:20         | 00:01:15           | 00:01:30         |
    | 00:01:00 | 00:01:30 |             |  00:00:20 | 00:00:15    | 00:00:35  | 00:01:00       | 00:01:30     | 00:01:00           | 00:01:20         | 00:01:15           | 00:01:30         |


  # These cases involve body duration and availability time cases, in which the logic significantly changes
  # The code assumes availability_time to be 0 unless specified otherwise.

  Scenario: Body timing parameters affecting document
    Given an xml file <xml_file>
    When it has sequenceIdentifier <sequence_identifier>
    And it has sequenceNumber <sequence_number>
    And it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body duration <body_dur>
    And it has body end time <body_end>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    And it is available at <availability_time>
    And the document is generated
    Then body active begin time is <body_active_begin>
    And body active end time is <body_active_end>
    And div active begin time is <div_active_begin>
    And div active end time is <div_active_end>

    Examples:
    | body_begin | body_dur | body_end | div_begin | div_end  | availability_time | body_active_begin | body_active_end | div_active_begin | div_active_end |
    |            |          |          |           |          |                   | 00:00:00          | undefined       | 00:00:00         | undefined      |
    |            |          |          |           |          | 00:00:05          | 00:00:05          | undefined       | 00:00:05         | undefined      |
    |            | 00:01:00 |          |           |          |                   | 00:00:00          | 00:01:00        | 00:00:00         | 00:01:00       |
    |            | 00:01:00 |          |           |          | 00:00:05          | 00:00:05          | 00:01:05        | 00:00:05         | 00:01:05       |
    |            | 00:01:00 | 00:00:50 |           |          |                   | 00:00:00          | 00:00:50        | 00:00:00         | 00:00:50       |
@skip
# Skipping tests where body has dur and there's a div with times because denester doesn't deal with them yet.
    |            | 00:00:05 |          | 01:00:00  |          |                   | 01:00:00          | 01:00:05        | 01:00:00         | 01:00:05       |
    |            | 00:00:05 |          | 00:00:05  | 00:00:12 |                   | 00:00:05          | 00:00:10        | 00:00:05         | 00:00:10       |
    
