@timing @resolution @document
Feature: Computed times computation

  # This tests mostly operates on document computed begin and end times. It does not deal with active duration of
  # child elements.

  Examples:
  | xml_file                                       | sequence_identifier | sequence_number |  
  | computed_resolved_time_semantics_empty_doc.xml | testSequence1       | 1               |  


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
