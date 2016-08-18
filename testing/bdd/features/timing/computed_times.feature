@timing @resolution @document
Feature: Computed times computation

  # This tests mostly operates on document computed begin and end times. It does not deal with active duration of
  # child elements.

  Examples:
  | xml_file                             | sequence_identifier | sequence_number |
  | computed_resolved_time_semantics.xml | testSequence1       | 1               |

  # SPEC-CONFORMANCE: R16 R17
  Scenario: Computed times of a document
    Given an xml file <xml_file>
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has sequenceNumber <sequence_number>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    And it has span2 begin time <span2_begin>
    And it has span2 end time <span2_end>
    And it has span3 begin time <span3_begin>
    And it has span3 end time <span3_end>
    And the document is generated  # implicitly means it is valid.
    And it has availability time <avail_time>
    Then it has computed begin time <computed_begin>
    And it has computed end time <computed_end>

    Examples:
    | time_base | body_begin  | body_end     | body_dur | div_begin   | div_end     | p_begin    | p_end      | span_begin  | span_end    | span2_begin | span2_end  | span3_begin | span3_end | computed_begin | computed_end | avail_time  |
    | clock     | 00:00:10.0  |              |          |             |             |            |            |             |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    | clock     |             | 00:00:10.0   |          |             |             |            |            |             |             |             |            |             |           | 00:00:00.0     | 00:00:10.0   | 00:00:00.0  |
    | clock     | 00:00:10.0  |              | 1h       |             |             |            |            |             |             |             |            |             |           | 00:00:10.0     | 01:00:10.0   | 00:00:00.0  |
    | clock     | 00:00:10.0  | 00:00:20.0   |          |             |             |            |            |             |             |             |            |             |           | 00:00:10.0     | 00:00:20.0   | 00:00:00.0  |
    | media     | 109:01:00.0 | 110:12:00.15 |          |             |             |            |            |             |             |             |            |             |           | 109:01:00.0    | 110:12:00.15 | 109:00:00.0 |
    | media     | 109:00:10.0 | 109:10:00.0  | 5m       |             |             |            |            |             |             |             |            |             |           | 109:00:10.0    | 109:05:10.0  | 109:00:00.0 |
    | clock     | 00:00:10.0  |              |          |             |             | 00:00:15.0 |            |             |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          |             |             |            | 00:00:05.0 |             |             |             |            |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          |             |             |            |            | 00:00:15.0  |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          |             |             |            |            |             | 00:00:05.0  |             |            |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    | clock     |             |              |          | 00:02:15.50 |             |            |            | 00:00:00.10 | 00:00:15.10 |             |            |             |           | 00:02:15.50    | 00:02:30.60  | 00:01:00.50 |
    | clock     | 00:00:10.0  | 00:00:20.0   |          |             |             |            | 00:00:30.0 |             |             |             |            |             |           | 00:00:10.0     | 00:00:20.0   | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          | 00:00:12.64 |             | 00:00:05.0 |            | 00:00:10.0  | 00:00:20.0  |             |            |             |           | 00:00:10.0     | 00:00:47.64  | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          | 00:00:12.64 |             |            |            | 00:00:10.0  | 00:00:20.0  |             |            |             |           | 00:00:10.0     | 00:00:42.64  | 00:00:00.0  |
    | clock     |             |              |          |             |             |            |            |             |             |             |            |             |           | 10:00:00.0     |              | 10:00:00.0  |
    | clock     |             |              |          | 10:58:00.0  |             |            |            | 00:02:00.0  | 00:10:00.0  |             |            |             |           | 10:58:00.0     | 11:08:00.0   | 10:00:00.0  |
    | clock     | 00:01:00.0  |              |          |             |             |            |            | 00:00:10.0  | 00:00:30.0  | 00:00:15.0  | 00:00:40.0 |             |           | 00:01:00.0     | 00:01:40.0   | 00:00:00.0  |
    | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:30.0  | 00:00:15.0  | 00:00:40.0 |             |           | 00:00:10.0     | 00:00:40.0   | 00:00:00.0  |
    | clock     |             |              |          |             |             |            |            | 00:00:15.0  | 00:00:30.0  | 00:00:10.0  | 00:00:40.0 |             |           | 00:00:10.0     | 00:00:40.0   | 00:00:00.0  |
    | clock     |             |              |          |             |             |            |            | 00:00:15.0  | 00:00:30.0  | 00:00:10.0  | 00:00:40.0 | 00:00:05.0  | 00:00:14.0| 00:00:05.0     | 00:00:40.0   | 00:00:00.0  |
    | clock     |             |              |          |             |             |            |            | 00:00:15.0  | 00:00:30.0  | 00:00:05.0  | 00:00:40.0 | 00:00:10.0  | 00:00:14.0| 00:00:05.0     | 00:00:40.0   | 00:00:00.0  |
    @skip
    | clock     | 00:00:10.0  |              | 5m       |             | 00:10:00.0  |            |            |             |             |             |            |             |           | 00:00:10.0     | 00:05:10.0   | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          | 00:00:15.0  |             |            |            |             |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    | clock     | 00:00:10.0  |              |          |             | 00:00:05.0  |            |            |             |             |             |            |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    | clock     |             |              |          | 00:02:15.50 | 01:05:40.60 |            |            |             |             |             |            |             |           | 00:02:15.50    | 01:05:40.60  | 00:01:00.50 |
