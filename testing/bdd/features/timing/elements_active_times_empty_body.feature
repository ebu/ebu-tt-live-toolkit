@timing @resolution @element
Feature: Computed element active begin and end times
  # Assuming that parent end = min(explicit end, begin+dur) where dur may exist, i.e. for body element.

  Scenario Outline: 

  # Given a parent element with one child element, the computed active parent and child begin and active parent end times are valid:
  Scenario Outline: Parent with no child element
    Given an xml file "elements_active_time_semantics_empty_body.xml"
    When it has sequenceIdentifier testSeq
    And it has sequenceNumber 1
    And it has timeBase media
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And the document is generated
    Then body active begin time is <body_active_begin>
    And body active end time is <body_active_end>

    Examples:
    | body_begin | body_end | body_active_begin | body_active_end | 
    |            |          | 00:00:00          | undefined       | 
    | 00:01:00   |          | 00:01:00          | undefined       | 
    |            | 00:01:30 | 00:00:00          | 00:01:30        | 
    | 00:01:00   | 00:01:30 | 00:01:00          | 00:01:30        | 


  # These cases involve body duration and availability time cases, in which the logic significantly changes
  # The code assumes availability_time to be 0 unless specified otherwise.
  Scenario Outline: Body timing parameters affecting document without children
    Given an xml file "elements_active_time_semantics_empty_body.xml"
    When it has sequenceIdentifier testSeq
    And it has sequenceNumber 1
    And it has timeBase media
    And it has body begin time <body_begin>
    And it has body duration <body_dur>
    And it has body end time <body_end>
    And the document is generated
    And it is available at <availability_time>
    Then body active begin time is <body_active_begin>
    And body active end time is <body_active_end>

    Examples:
    | body_begin | body_dur | body_end | availability_time | body_active_begin | body_active_end |
    |            |          |          |                   | 00:00:00          | undefined       |
    |            |          |          | 00:00:05          | 00:00:05          | undefined       |
    |            | 00:01:00 |          |                   | 00:00:00          | 00:01:00        |
    |            | 00:01:00 |          | 00:00:05          | 00:00:05          | 00:01:05        |
    |            | 00:01:00 | 00:00:50 |                   | 00:00:00          | 00:00:50        |
