@timing @resolution @sequence
Feature: Resolved times computation in sequence

  # SPEC-CONFORMANCE: R15 R16 R17
  # Also validates that resolved times don't overlap, which tests SPEC-CONFORMANCE R1 R13 R14
  # To test missing <body>, the template has: {% if not body %}
  # For backwards compatibility, TRUE equals no body. 
  # Nunjunks interprets true/false as a string, so in the examples an empty variable is FALSE. Any other value is TRUE 
  Scenario Outline: Resolved times in sequence
    Given a sequence with the following identifier and timeBase
      | sequence_identifier | time_base |
      | testSequence1       | clock     |
    And an xml file "computed_resolved_time_semantics.xml"
    And it has the following template variables
      | sequence_identifier | sequence_number | time_base | body_begin  | body_end   | body_dur | body |
      | testSequence1       | 1               | clock     | 00:00:10.0  | 00:00:20.0 |          |      |
    And doc1 is added to the sequence with availability time "00:00:01.0"
    When we create a new document
    And it has the following template variables
      | sequence_identifier | sequence_number | time_base | body_begin | body_end | body_dur  | body |
      | testSequence1       | 2               | clock     | 00:00:30.0 |          | 10s       |      |
    And doc2 is added to the sequence with availability time "00:00:05.0"
    And we create a new document
    And it has sequenceIdentifier "testSequence1"
    And it has timeBase "clock"
    And it has predefined sequenceNumber 3
    And it has doc3 body <doc3_no_body>
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc1 has resolved begin time <r_begin_doc1>
    And doc1 has resolved end time <r_end_doc1>
    And doc2 has resolved begin time <r_begin_doc2>
    And doc2 has resolved end time <r_end_doc2>
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_no_body | doc3_begin | doc3_end   | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc2 | r_end_doc2 | r_begin_doc3 | r_end_doc3 |  
    | 00:00:20.0      |              | 00:00:50.0 | 00:01:00.0 |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |  
    | 00:00:03.0      |              | 00:00:50.0 | 00:01:00.0 |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |  
    | 00:00:20.0      |              | 00:00:35.0 | 00:01:00.0 |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:35.0 | 00:00:35.0   | 00:01:00.0 |  


  # SPEC-CONFORMANCE: R15 R16 R17
  Scenario Outline: Resolved times in sequence, document 2 skipped
    Given a sequence with the following identifier and timeBase
    | sequence_identifier | time_base |
    | testSequence1       | clock     |
    And an xml file "computed_resolved_time_semantics.xml"
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body_begin  | body_end   | body_dur | body |
    | testSequence1       | 1               | clock     | 00:00:10.0  | 00:00:20.0 |          |      |
    And doc1 is added to the sequence with availability time "00:00:01.0"
    When we create a new document
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body_begin | body_end | body_dur  | body | doc3_no_body|
    | testSequence1       | 2               | clock     | 00:00:30.0 |          | 10s       |      |             |
    And doc2 is added to the sequence with availability time "00:00:05.0"
    And we create a new document
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body |
    | testSequence1       | 3               | clock     |      |
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc2 has resolved_end < resolved_begin and is skipped
    And doc1 has resolved begin time <r_begin_doc1>
    And doc1 has resolved end time <r_end_doc1>
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin | doc3_end   | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc3 | r_end_doc3 |  
    | 00:00:02.0      | 00:00:25.0 | 00:01:00.0 |          | 00:00:10.0   | 00:00:20.0 | 00:00:25.0   | 00:01:00.0 |  
    | 00:00:15.0      | 00:00:16.0 | 00:00:35.0 |          | 00:00:10.0   | 00:00:16.0 | 00:00:16.0   | 00:00:35.0 |  


  # SPEC-CONFORMANCE: R15 R16 R17
  Scenario Outline: Resolved times in sequence, document 1 and 2 skipped
    Given a sequence with the following identifier and timeBase
    | sequence_identifier | time_base |
    | testSequence1       | clock     |
    And an xml file "computed_resolved_time_semantics.xml"
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body_begin  | body_end   | body_dur | body |
    | testSequence1       | 1               | clock     | 00:00:10.0  | 00:00:20.0 |          |      |
    And doc1 is added to the sequence with availability time "00:00:01.0"
    When we create a new document
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body_begin | body_end | body_dur  | body | doc3_no_body|
    | testSequence1       | 2               | clock     | 00:00:30.0 |          | 10s       |      |             |
    And doc2 is added to the sequence with availability time "00:00:05.0"
    And we create a new document
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body |
    | testSequence1       | 3               | clock     |      |
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc1 and doc2 have resolved_end < resolved_begin and are skipped
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin  | doc3_end | doc3_dur | r_begin_doc3 | r_end_doc3  |  
    | 00:00:08.0      | 00:00:09.23 |          | 1h       | 00:00:09.23  | 01:00:09.23 |  
    | 00:00:00.0      | 00:00:09.0  |          | 1h       | 00:00:09.0   | 01:00:09.0  |  
    | 00:00:00.0      | 00:00:04.0  |          | 1h       | 00:00:04.0   | 01:00:04.0  |  


  # SPEC-CONFORMANCE: R16 R17
  Scenario Outline: Out of order delivery of documents (applicable with some carriage mechanisms)
    Given a sequence with the following identifier and timeBase
    | sequence_identifier | time_base |
    | testSequence1       | clock     |
    And an xml file "computed_resolved_time_semantics.xml"
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body_begin  | body_end   | body_dur | body |
    | testSequence1       | 1               | clock     | 00:00:10.0  | 00:00:20.0 |          |      |
    And doc1 is added to the sequence with availability time "00:00:01.0"
    When we create a new document
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body |
    | testSequence1       | 3               | clock     |      |
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    And we create a new document
    And it has the following template variables
    | sequence_identifier | sequence_number | time_base | body_begin | body_end | body_dur  | body | doc3_no_body|
    | testSequence1       | 2               | clock     | 00:00:30.0 |          | 10s       |      |             |
    And doc2 is added to the sequence with availability time "00:00:05.0"
    Then doc1 has resolved begin time <r_begin_doc1>
    And doc1 has resolved end time <r_end_doc1>
    And doc2 has resolved begin time <r_begin_doc2>
    And doc2 has resolved end time <r_end_doc2>
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin | doc3_end   | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc2 | r_end_doc2 | r_begin_doc3 | r_end_doc3 |  
    | 00:00:03.0      | 00:00:50.0 | 00:01:00.0 |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |  
    | 00:00:03.0      | 00:00:38.0 | 00:01:00.0 |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:38.0 | 00:00:38.0   | 00:01:00.0 |  
