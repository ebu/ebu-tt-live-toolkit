@timing @delay
Feature: Delay of a document sequence

  Examples:
  | xml_file      |
  | delayNode.xml |  # Empty span timing creates the span without timing. It does not omit it.

  #TBC: this is a change to the spec (passive delay node)
  @skip
  Scenario: BufferDelayNode, unchanged sequence identifier
    Given an xml file <xml_file>
    And the document is generated
    And sequence identifier <sequence_id_1>
    When the delay node delays it by <delay>
    Then the delayed document has <sequence_id_2>

    Examples:
    | sequence_id_1 | delay      | sequence_id_2 |
    | 1             | 00:00:02.0 | 1             |
    | xxx           | 00:00:00   | xxx           |
    | 99999999999   | 99:00:00   | 99999999999   |

  # SPEC-CONFORMANCE.md R114    
  # Times are inherited so to delay an element we only need to delay its syncbase  
  Scenario: RetimingDelayNode delays document, computed times
    Given an xml file <xml_file>
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
    And the document is generated
    When the retiming delay node delays it by <delay>
    Then the updated body computed begin time is <updated_body_begin>
    And the updated body computed end time is <updated_body_end>
    And the updated div computed begin time is <updated_div_begin>
    And the updated div computed end time is <updated_div_end>
    And the updated p computed begin time is <updated_p_begin>
    And the updated p computed end time is <updated_p_end>
    And the updated span computed begin time is <updated_span_begin>
    And the updated span computed end time is <updated_span_end>
    And the updated span2 computed begin time is <updated_span2_begin>
    And the updated span2 computed end time is <updated_span2_end>


    Examples:
    | body_begin | body_end     | div_begin | div_end  | p_begin  | p_end    | span_begin | span_end | span2_begin | span2_end | delay    | updated_body_begin | updated_body_end | updated_div_begin | updated_div_end | updated_p_begin | updated_p_end | updated_span_begin | updated_span_end | updated_span2_begin | updated_span2_end | body_dur |
    | 00:00:05   |              |           |          |          |          |            |          |             |           | 00:00:10 | 00:00:15           |                  | 00:00:15          |                 | 00:00:15        |               | 00:00:15           |                  | 00:00:15            |                   |          |
    |            | 00:00:05     |           |          |          |          |            |          |             |           | 00:00:10 | 00:00:10           | 00:00:15         | 00:00:10          | 00:00:15        | 00:00:10        | 00:00:15      | 00:00:10           | 00:00:15         | 00:00:10            | 00:00:15          |          |
    | 00:00:05   | 00:00:06     |           |          |          |          |            |          |             |           | 00:00:10 | 00:00:15           | 00:00:16         | 00:00:15          | 00:00:16        | 00:00:15        | 00:00:16      | 00:00:15           | 00:00:16         | 00:00:15            | 00:00:16          |          |
    | 00:00:05   | 00:00:20     |           |          |          |          |            |          |             |           | 00:00:00 | 00:00:05           | 00:00:20         | 00:00:05          | 00:00:20        | 00:00:05        | 00:00:20      | 00:00:05           | 00:00:20         | 00:00:05            | 00:00:20          |          |
    |            |              | 00:00:05  |          |          |          |            |          |             |           | 00:00:10 | 00:00:15           |                  | 00:00:15          |                 | 00:00:15        |               | 00:00:15           |                  | 00:00:15            |                   |          |
    |            |              |           | 00:00:05 |          |          |            |          |             |           | 00:00:10 | 00:00:10           | 00:00:15         | 00:00:10          | 00:00:15        | 00:00:10        | 00:00:15      | 00:00:10           | 00:00:15         | 00:00:10            | 00:00:15          |          |
    |            |              | 00:00:05  | 00:00:08 |          |          |            |          |             |           | 00:00:10 | 00:00:15           | 00:00:18         | 00:00:15          | 00:00:18        | 00:00:15        | 00:00:18      | 00:00:15           | 00:00:18         | 00:00:15            | 00:00:18          |          |
    |            |              |           |          | 00:00:05 |          |            |          |             |           | 00:00:10 | 00:00:15           |                  | 00:00:15          |                 | 00:00:15        |               | 00:00:15           |                  | 00:00:15            |                   |          |
    |            |              |           |          |          | 00:00:05 |            |          |             |           | 00:00:10 | 00:00:10           | 00:00:15         | 00:00:10          | 00:00:15        | 00:00:10        | 00:00:15      | 00:00:10           | 00:00:15         | 00:00:10            | 00:00:15          |          |
    |            |              |           |          | 00:00:05 | 00:00:08 |            |          |             |           | 00:00:10 | 00:00:15           | 00:00:18         | 00:00:15          | 00:00:18        | 00:00:15        | 00:00:18      | 00:00:15           | 00:00:18         | 00:00:15            | 00:00:18          |          |
    | 00:00:05   | 00:00:20     | 00:00:03  |          |          |          |            |          |             |           | 00:00:05 | 00:00:10           | 00:00:25         | 00:00:13          | 00:00:25        | 00:00:13        | 00:00:25      | 00:00:13           | 00:00:25         | 00:00:13            | 00:00:25          |          |
    | 00:00:05   | 00:00:20     | 00:00:03  |          | 00:00:04 |          |            |          |             |           | 00:00:05 | 00:00:10           | 00:00:25         | 00:00:13          | 00:00:25        | 00:00:17        | 00:00:25      | 00:00:17           | 00:00:25         | 00:00:17            | 00:00:25          |          |
    | 00:00:10   | 00:00:10.500 |           |          | 00:00:03 | 00:00:06 |            |          |             |           | 01:00:00 | 01:00:10           | 01:00:10.500     | 01:00:13          | 01:00:10.500    | 01:00:13        | 01:00:10.500  | 01:00:13           | 01:00:10.500     | 01:00:13            | 01:00:10.500      |          |
    |            |              | 00:00:10  | 00:00:20 | 00:00:05 | 00:00:07 |            |          |             |           | 00:00:01 | 00:00:11           | 00:00:21         | 00:00:11          | 00:00:21        | 00:00:16        | 00:00:18      | 00:00:16           | 00:00:18         | 00:00:16            | 00:00:18          |          |
    |            |              |           | 00:00:20 |          | 00:00:10 |            |          |             |           | 00:00:15 | 00:00:15           | 00:00:35         | 00:00:15          | 00:00:35        | 00:00:15        | 00:00:25      | 00:00:15           | 00:00:25         | 00:00:15            | 00:00:25          |          |
    |            |              | 00:00:20  |          |          | 00:00:10 |            |          |             |           | 00:00:15 | 00:00:35           | 00:00:45         | 00:00:35          | 00:00:45        | 00:00:35        | 00:00:45      | 00:00:35           | 00:00:45         | 00:00:35            | 00:00:45          |          |


  Scenario: RetimingDelayNode delays document, specified times
    Given an xml file <xml_file>
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
    And the document is generated
    When the retiming delay node delays it by <delay>
    Then the updated body specified begin time is <updated_body_begin>
    And the updated body specified end time is <updated_body_end>
    And the updated div specified begin time is <updated_div_begin>
    And the updated div specified end time is <updated_div_end>
    And the updated p specified begin time is <updated_p_begin>
    And the updated p specified end time is <updated_p_end>
    And the updated span specified begin time is <updated_span_begin>
    And the updated span specified end time is <updated_span_end>
    And the updated span2 specified begin time is <updated_span2_begin>
    And the updated span2 specified end time is <updated_span2_end>


    Examples:
    | body_begin | body_end     | div_begin | div_end  | p_begin  | p_end    | span_begin | span_end | span2_begin | span2_end | delay    | updated_body_begin | updated_body_end | updated_div_begin | updated_div_end | updated_p_begin | updated_p_end | updated_span_begin | updated_span_end | updated_span2_begin | updated_span2_end | body_dur |
    | 00:00:05   |              |           |          |          |          |            |          |             |           | 00:00:10 | 00:00:15           |                  |                   |                 |                 |               |                    |                  |                     |                   |          |
    |            |              |           |          |          |          | 00:00:20   |          |             |           | 00:00:05 | 00:00:05           |                  |                   |                 |                 |               | 00:00:20           |                  |                     |                   |          |
    |            |              |           |          |          |          | 00:00:20   |          | 00:00:20    |           | 00:00:05 |                    |                  |                   |                 |                 |               | 00:00:25           |                  | 00:00:25            |                   |          |
    |            | 00:00:05     |           |          |          |          |            |          |             |           | 00:00:10 | 00:00:10           | 00:00:15         |                   |                 |                 |               |                    |                  |                     |                   |          |
    | 00:00:05   | 00:00:06     |           |          |          |          |            |          |             |           | 00:00:10 | 00:00:15           | 00:00:16         |                   |                 |                 |               |                    |                  |                     |                   |          |
    | 00:00:05   | 00:00:20     |           |          |          |          |            |          |             |           | 00:00:00 | 00:00:05           | 00:00:20         |                   |                 |                 |               |                    |                  |                     |                   |          |
    |            |              | 00:00:05  |          |          |          |            |          |             |           | 00:00:10 |                    |                  | 00:00:15          |                 |                 |               |                    |                  |                     |                   |          |
    |            |              |           | 00:00:05 |          |          |            |          |             |           | 00:00:10 | 00:00:10           |                  |                   | 00:00:05        |                 |               |                    |                  |                     |                   |          |
    |            |              | 00:00:05  | 00:00:08 |          |          |            |          |             |           | 00:00:10 |                    |                  | 00:00:15          | 00:00:18        |                 |               |                    |                  |                     |                   |          |
    |            |              |           |          | 00:00:05 |          |            |          |             |           | 00:00:10 |                    |                  |                   |                 | 00:00:15        |               |                    |                  |                     |                   |          |
    |            |              |           |          |          | 00:00:05 |            |          |             |           | 00:00:10 | 00:00:10           |                  |                   |                 |                 | 00:00:05      |                    |                  |                     |                   |          |
    |            |              |           |          | 00:00:05 | 00:00:08 |            |          |             |           | 00:00:10 |                    |                  |                   |                 | 00:00:15        | 00:00:18      |                    |                  |                     |                   |          |
    |            |              |           |          |          |          | 00:00:05   |          |             |           | 00:00:10 | 00:00:10           |                  |                   |                 |                 |               | 00:00:05           |                  |                     |                   |          |
    |            |              |           |          |          |          |            | 00:00:05 |             |           | 00:00:10 | 00:00:10           |                  |                   |                 |                 |               |                    | 00:00:05         |                     |                   |          |
    |            |              |           |          |          |          | 00:00:05   | 00:00:08 |             |           | 00:00:10 | 00:00:10           |                  |                   |                 |                 |               | 00:00:05           | 00:00:08         |                     |                   |          |
    |            |              |           |          |          |          |            |          | 00:00:05    |           | 00:00:10 | 00:00:10           |                  |                   |                 |                 |               |                    |                  | 00:00:05            |                   |          |
    |            |              |           |          |          |          |            |          |             | 00:00:05  | 00:00:10 | 00:00:10           |                  |                   |                 |                 |               |                    |                  |                     | 00:00:05          |          |
    |            |              |           |          |          |          |            |          | 00:00:05    | 00:00:08  | 00:00:10 | 00:00:10           |                  |                   |                 |                 |               |                    |                  | 00:00:05            | 00:00:08          |          |
    | 00:00:05   | 00:00:20     | 00:00:03  |          |          |          |            |          |             |           | 00:00:05 | 00:00:10           | 00:00:25         | 00:00:03          |                 |                 |               |                    |                  |                     |                   |          |
    | 00:00:05   | 00:00:20     | 00:00:03  |          | 00:00:04 |          |            |          |             |           | 00:00:05 | 00:00:10           | 00:00:25         | 00:00:03          |                 | 00:00:04        |               |                    |                  |                     |                   |          |
    | 00:00:10   | 00:00:10.500 |           |          | 00:00:03 | 00:00:06 |            |          |             |           | 01:00:00 | 01:00:10           | 01:00:10.500     |                   |                 | 00:00:03        | 00:00:06      |                    |                  |                     |                   |          |
    |            |              | 00:00:10  | 00:00:20 | 00:00:05 | 00:00:07 |            |          |             |           | 00:00:01 |                    |                  | 00:00:11          | 00:00:21        | 00:00:05        | 00:00:07      |                    |                  |                     |                   |          |
    |            |              |           | 00:00:20 |          | 00:00:10 |            |          |             |           | 00:00:15 | 00:00:15           |                  |                   | 00:00:20        |                 | 00:00:10      |                    |                  |                     |                   |          |
    |            |              | 00:00:20  |          |          | 00:00:10 |            |          |             |           | 00:00:15 |                    |                  | 00:00:35          |                 |                 | 00:00:10      |                    |                  |                     |                   |          |
    |            |              |           |          |          |          |            |          |             |           | 00:00:05 | 00:00:05           |                  |                   |                 |                 |               |                    |                  |                     |                   |          |


    # SPEC-CONFORMANCE.md R113 R117
    Scenario: RetimingDelayNode changes sequence ID but not authoring delay
        Given an xml file <xml_file>
        And it has <sequence_id_1>
        And it has <authoring_delay_1>
        And the document is generated
        When the retiming delay node delays it by <delay>
        Then the updated document has <sequence_id_2>
        And the updated document has  <authoring_delay_2>

        Examples:
        | sequence_id_1 | authoring_delay_1 | delay    | sequence_id_2 | authoring_delay_2 |  
        | id1           | 00:00:00          | 0        | id2           | 00:00:00          |  
        | 0             | 00:00:05          | 00:00:03 | 1             | 00:00:05          |  
        | 0             |                   | 00:00:03 | 1             |                   |  


      
