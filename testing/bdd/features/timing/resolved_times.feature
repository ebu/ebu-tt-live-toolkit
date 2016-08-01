@timing @timingresolution
Feature: Resolved times computation

  # SPEC-CONFORMANCE:
  Scenario: Resolved times on a single document
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has sequenceNumber <sequence_number>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    And the document is generated  # implicitly means it is valid.
    And it has availability time <avail_time>
    Then it has resolved begin time <resolved_begin>
    And it has resolved end time <resolved_end>

    Examples:
    | xml_file                 | time_base | sequence_number | body_begin  | body_end     | body_dur | resolved_begin | resolved_end | avail_time  |
    | timeBase_timeformat.xml  | clock     | 1               | 00:00:10.0  |              |          | 00:00:10.0     |              | 00:00:00.0  |
    | timeBase_timeformat.xml  | clock     | 1               |             | 00:00:10.0   |          | 00:00:00.0     |              | 00:00:00.0  |
    | timeBase_timeformat.xml  | clock     | 1               | 00:00:10.0  |              | 1h       | 00:00:10.0     | 01:00:10.0   | 00:00:00.0  |
    | timeBase_timeformat.xml  | clock     | 1               | 00:00:10.0  | 00:00:20.0   |          | 00:00:10.0     | 00:00:20.0   | 00:00:00.0  |
    | timeBase_timeformat.xml  | media     | 1               | 109:01:00.0 | 110:12:00.15 |          | 109:01:00.0    | 110:12:00.15 | 109:00:00.0 |
    | timeBase_timeformat.xml  | media     | 1               | 109:00:10.0 | 109:10:00.0  | 5m       | 109:00:10.0    | 109:05:10.0  | 109:00:00.0 |
