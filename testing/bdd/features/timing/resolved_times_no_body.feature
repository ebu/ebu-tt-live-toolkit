@timing @resolution @sequence
Feature: Resolved times computation in sequence when there is no body

  Examples:
  | xml_file                             | sequence_identifier | time_base |
  | computed_resolved_time_semantics.xml | testSequence1       | clock     |

  # SPEC-CONFORMANCE: R15 R16 R17
  # Also validates that resolved times don't overlap, which tests SPEC-CONFORMANCE R1 R13 R14
  # To test missing <body>, the template has: {% if not body %}
  # For backwards compatibility, TRUE equals no body. 
  # Nunjunks interprets true/false as a string, so in the examples an empty variable is FALSE. Any other value is TRUE 
  Scenario: Resolved times in sequence
    Given a sequence <sequence_identifier> with timeBase <time_base>
    And an xml file <xml_file>
    When it has predefined sequenceNumber 1
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has doc1 body <doc1_no_body>
    And it has doc1 body begin time <doc1_begin>
    And it has doc1 body end time <doc1_end>
    And it has doc1 body duration <doc1_dur>
    And doc1 is added to the sequence with availability time <doc1_avail_time>
    And we create a new document
    And it has predefined sequenceNumber 2
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has doc2 body <doc2_no_body>
    And it has doc2 body begin time <doc2_begin>
    And it has doc2 body end time <doc2_end>
    And it has doc2 body duration <doc2_dur>
    And doc2 is added to the sequence with availability time <doc2_avail_time>
    And we create a new document
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
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
    | doc1_avail_time | doc1_no_body | doc1_begin | doc1_end | doc1_dur | doc2_avail_time | doc2_no_body | doc2_begin | doc2_end | doc2_dur | doc3_avail_time | doc3_no_body | doc3_begin | doc3_end | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc2 | r_end_doc2 | r_begin_doc3 | r_end_doc3 |  
    #This example passes only when the resolved doc1_end is NULL instead of 00:00:00. To be investigated. This is probably a bug. 
    | 00:00:00.0      | TRUE         |            |          |          | 00:00:01.0      | TRUE         |            |          |          | 00:00:03.0      | TRUE         |            |          |          | 00:00:00.0   |            | 00:00:01.0   | 00:00:01.0 | 00:00:03.0   | 00:00:03.0 |  
    | 00:00:00.1      |              | 00:00:10   | 00:00:15 |          | 00:00:00.2      |              | 00:00:20   | 00:00:25 |          | 00:00:00.3      | TRUE         |            |          |          | 00:00:10.0   | 00:00:00.3 | 00:00:20.0   | 00:00:00.3 | 00:00:00.3   | 00:00:00.3 |  
    | 00:00:00        |              | 00:00:00   | 00:00:10 |          | 00:00:05        | TRUE         |            |          |          | 00:00:10        |              | 00:00:10   | 00:00:20 |          | 00:00:00     | 00:00:05   | 00:00:05     | 00:00:05   | 00:00:10     | 00:00:20   |  
    | 00:00:10        | TRUE         |            |          |          | 00:00:05        |              | 00:00:10   | 00:00:20 |          | 00:00:20        |              |            |          |          | 00:00:10     | 00:00:10   | 00:00:10     | 00:00:20   | 00:00:20     |            |  
   

  