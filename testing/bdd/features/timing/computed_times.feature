@timing @resolution @document
Feature: Computed times computation

  # This tests mostly operates on document computed begin and end times. It does not deal with active duration of
  # child elements.

  Examples:
  | xml_file                             | sequence_identifier | sequence_number | no_body |
  | computed_resolved_time_semantics.xml | testSequence1       | 1               |         |

  # SPEC-CONFORMANCE: R16 R17 R132
  Scenario: Computed times of a document
    Given an xml file <xml_file>
    And l is <l>
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has sequenceNumber <sequence_number>
    And it has body <no_body>
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
    |  l | time_base | body_begin  | body_end     | body_dur | div_begin   | div_end     | p_begin    | p_end      | span_begin  | span_end    | span2_begin | span2_end  | span3_begin | span3_end | computed_begin | computed_end | avail_time  |
    |  1 | clock     | 00:00:10.0  |              |          |             |             |            |            |             |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    |  2 | clock     |             | 00:00:10.0   |          |             |             |            |            |             |             |             |            |             |           | 00:00:00.0     | 00:00:10.0   | 00:00:00.0  |
    |  3 | clock     | 00:00:10.0  |              | 1h       |             |             |            |            |             |             |             |            |             |           | 00:00:10.0     | 01:00:10.0   | 00:00:00.0  |
    |  4 | clock     | 00:00:10.0  | 00:00:20.0   |          |             |             |            |            |             |             |             |            |             |           | 00:00:10.0     | 00:00:20.0   | 00:00:00.0  |
    |  5 | media     | 109:01:00.0 | 110:12:00.15 |          |             |             |            |            |             |             |             |            |             |           | 109:01:00.0    | 110:12:00.15 | 109:00:00.0 |
    |  6 | media     | 109:00:10.0 | 109:10:00.0  | 5m       |             |             |            |            |             |             |             |            |             |           | 109:00:10.0    | 109:05:10.0  | 109:00:00.0 |
    |  7 | clock     | 00:00:10.0  |              |          |             |             | 00:00:15.0 |            |             |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    |  8 | clock     | 00:00:10.0  |              |          |             |             |            | 00:00:05.0 |             |             |             |            |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    |  9 | clock     | 00:00:10.0  |              |          |             |             |            |            | 00:00:15.0  |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    | 10 | clock     | 00:00:10.0  |              |          |             |             |            |            |             | 00:00:05.0  |             |            |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    | 11 | clock     |             |              |          | 00:02:15.50 |             |            |            | 00:00:00.10 | 00:00:15.10 |             |            |             |           | 00:02:15.50    | 00:02:30.60  | 00:01:00.50 |
    | 12 | clock     | 00:00:10.0  | 00:00:20.0   |          |             |             |            | 00:00:30.0 |             |             |             |            |             |           | 00:00:10.0     | 00:00:20.0   | 00:00:00.0  |
    | 13 | clock     | 00:00:10.0  |              |          | 00:00:12.64 |             | 00:00:05.0 |            | 00:00:10.0  | 00:00:20.0  |             |            |             |           | 00:00:10.0     | 00:00:47.64  | 00:00:00.0  |
    | 14 | clock     | 00:00:10.0  |              |          | 00:00:12.64 |             |            |            | 00:00:10.0  | 00:00:20.0  |             |            |             |           | 00:00:10.0     | 00:00:42.64  | 00:00:00.0  |
    | 15 | clock     |             |              |          |             |             |            |            |             |             |             |            |             |           | 10:00:00.0     |              | 10:00:00.0  |
    | 16 | clock     |             |              |          | 10:58:00.0  |             |            |            | 00:02:00.0  | 00:10:00.0  |             |            |             |           | 10:58:00.0     | 11:08:00.0   | 10:00:00.0  |
    | 17 | clock     | 00:01:00.0  |              |          |             |             |            |            | 00:00:10.0  | 00:00:30.0  | 00:00:15.0  | 00:00:40.0 |             |           | 00:01:00.0     | 00:01:40.0   | 00:00:00.0  |
    | 18 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:30.0  | 00:00:15.0  | 00:00:40.0 |             |           | 00:00:10.0     | 00:00:40.0   | 00:00:00.0  |
    | 19 | clock     |             |              |          |             |             |            |            | 00:00:15.0  | 00:00:30.0  | 00:00:10.0  | 00:00:40.0 |             |           | 00:00:10.0     | 00:00:40.0   | 00:00:00.0  |
    | 20 | clock     |             |              |          |             |             |            |            | 00:00:15.0  | 00:00:30.0  | 00:00:10.0  | 00:00:40.0 | 00:00:05.0  | 00:00:14.0| 00:00:05.0     | 00:00:40.0   | 00:00:00.0  |
    | 21 | clock     |             |              |          |             |             |            |            | 00:00:15.0  | 00:00:30.0  | 00:00:05.0  | 00:00:40.0 | 00:00:10.0  | 00:00:14.0| 00:00:05.0     | 00:00:40.0   | 00:00:00.0  |
    # The following scenarios are to deal with end times before the begin times. R132
    | 22 | clock     | 00:00:10.0  | 00:00:05.0   |          |             |             |            |            |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 23 | clock     |             |              |          | 00:00:10.0  | 00:00:05.0  |            |            |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 24 | clock     |             |              |          |             |             | 00:00:10.0 | 00:00:05.0 |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 25 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:05.0  |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 26 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:05.0  | 00:00:15.0  | 00:00:10.0 |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 27 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:05.0  | 00:00:15.0  | 00:00:10.0 | 00:00:05.0  | 00:00:01.0| 00:00:00.0     |              | 00:00:00.0  |
    # And as above but where there are also elements whose end times are after the begin times.
    | 28 | clock     | 00:00:10.0  | 00:00:05.0   |          | 00:00:10.0  | 00:00:15.0  |            |            |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 29 | clock     |             |              |          | 00:00:10.0  | 00:00:05.0  | 00:00:10.0 | 00:00:15.0 |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 30 | clock     |             |              |          |             |             | 00:00:10.0 | 00:00:05.0 | 00:00:10.0  | 00:00:15.0  |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 31 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:05.0  | 00:00:10.0  | 00:00:15.0 |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    | 32 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:05.0  | 00:00:15.0  | 00:00:10.0 | 00:00:10.0  | 00:00:15.0| 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    # And as above but where the begin value is equal to end value (begin is inclusive, end exclusive, so this still counts as "end before begin")
    | 33 | clock     | 00:00:10.0  | 00:00:10.0   |          |             |             |            |            |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 34 | clock     |             |              |          | 00:00:10.0  | 00:00:10.0  |            |            |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 35 | clock     |             |              |          |             |             | 00:00:10.0 | 00:00:10.0 |             |             |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 36 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:10.0  |             |            |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 37 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:10.0  | 00:00:15.0  | 00:00:15.0 |             |           | 00:00:00.0     |              | 00:00:00.0  |
    | 38 | clock     |             |              |          |             |             |            |            | 00:00:10.0  | 00:00:10.0  | 00:00:15.0  | 00:00:15.0 | 00:00:05.0  | 00:00:05.0| 00:00:00.0     |              | 00:00:00.0  |
    # The following scenarios check for correct processing of some unspecified begin or end times.
    | 39 | clock     | 00:00:10.0  |              | 5m       |             | 00:10:00.0  |            |            |             |             |             |            |             |           | 00:00:10.0     | 00:05:10.0   | 00:00:00.0  |
    | 40 | clock     | 00:00:10.0  |              |          | 00:00:15.0  |             |            |            |             |             |             |            |             |           | 00:00:10.0     |              | 00:00:00.0  |
    | 41 | clock     | 00:00:10.0  |              |          |             | 00:00:05.0  |            |            |             |             |             |            |             |           | 00:00:10.0     | 00:00:15.0   | 00:00:00.0  |
    | 42 | clock     |             |              |          | 00:02:15.50 | 01:05:40.60 |            |            |             |             |             |            |             |           | 00:02:15.50    | 01:05:40.60  | 00:01:00.50 |
