@timing @resolution @document
Feature: Computed times computation

  # This tests mostly operates on document computed begin and end times. It does not deal with active duration of
  # child elements.

  Examples:
  | xml_file                             | sequence_identifier | sequence_number |
  | computed_resolved_time_semantics.xml | testSequence1       | 1               |

  # SPEC-CONFORMANCE: R44
  # We test the computed times for an empty <body> but not the display since presentation is not in scope. 
  Scenario: Computed times of a document with empty body
    Given an xml file <xml_file>
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has sequenceNumber <sequence_number>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    And the document is generated  # implicitly means it is valid.
    And it has availability time <avail_time>
    Then it has computed begin time <computed_begin>
    And it has computed end time <computed_end>

    Examples:
    | time_base | body_begin  | body_end     | body_dur | avail_time  | computed_begin | computed_end | 
    | clock     | 00:00:10.0  |              |          | 00:00:00.0  | 00:00:10.0     |              | 
    | clock     |             | 00:00:10.0   |          | 00:00:00.0  | 00:00:00.0     | 00:00:10.0   | 
    | clock     | 00:00:10.0  |              | 1h       | 00:00:00.0  | 00:00:10.0     | 01:00:10.0   | 
    | clock     | 00:00:10.0  | 00:00:20.0   |          | 00:00:00.0  | 00:00:10.0     | 00:00:20.0   | 
    | media     | 109:01:00.0 | 110:12:00.15 |          | 109:00:00.0 | 109:01:00.0    | 110:12:00.15 | 
    | media     | 109:00:10.0 | 109:10:00.0  | 5m       | 109:00:00.0 | 109:00:10.0    | 109:05:10.0  | 


  # A document without <body>. This means no timings at all in the document since the <body> is the topmost element that accepts timing attributes.  
  # From TTML1: 
  # "The Root Temporal Extent, i.e., the time interval over which a Document Instance is active, 
  # has an implicit duration that is equal to ... zero if the body element is absent." 
  Scenario: Computed times of a document with empty body
    Given an xml file <xml_file>
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has sequenceNumber <sequence_number>
    And the document is generated  # implicitly means it is valid.
    And it has availability time <avail_time>
    Then it has computed begin time <computed_begin>
    And it has computed end time <computed_end>

    Examples:
    | time_base | avail_time  | computed_begin | computed_end |  
    | clock     | 00:00:00.0  | 00:00:00.0     | 00:00:00.0   |  
    | media     | 109:00:00.0 | 109:00:00.0    | 109:00:00.0  |  
