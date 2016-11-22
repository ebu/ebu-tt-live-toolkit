@timing @delay
Feature: Delay of a document sequence

  Examples:
  | xml_file      |
  | delayNode.xml |

  @skip
  Scenario: Implicitly timed document delay
    Given an xml file <xml_file>
    And the document is generated
    And it has availability time <avail_time>
    When the delay node delays it by <delay>
    Then the delay node outputs the document at <delayed_avail_time>

    Examples:
    | avail_time | delay      | delayed_avail_time |
    | 00:00:10.0 | 00:00:02.0 | 00:00:12.0         |
    | 00:00:10.0 | 00:00:00.0 | 00:00:10.0         |
    # Negative value should really throw an exception
    | 00:00:10.0 | -00:00:00  | 00:00:10.0         |  

#TODO: test that the order of documents in the input and output sequence is the same (FIFO) 


  #TBC: this is a change to the spec (passive delay node)
  Scenario: Implicitly timed document unchanged sequence identifier 
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
    # No document generated for negative delay
    | 1             | -00:00:01  |               |


  # Times are inherited so to delay an element we only need to delay its syncbase  
  Scenario: Explicitly timed document delay
    Given an xml file <xml_file>
    And the document is generated
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    And it has p begin time <p_begin>  
    And it has p end time <p_end>  
    When the delay node delays it by <delay>
    Then the document has body begin time <updated_body_begin>
    And it has body end time <updated_body_end>
    And it has div begin time <updated_div_begin>
    And it has div end time <updated_div_end>
    And it has p begin time <updated_p_begin>  
    And it has p end time <updated_p_end>  


    Examples:
    | body_begin | body_end     | div_begin | div_end  | p_begin  | p_end    | delay    | updated_body_begin | updated_body_end | updated_div_begin | updated_div_end | updated_p_begin | updated_p_end |  
    | 00:00:05   | 00:00:06     |           |          |          |          | 00:00:10 | 00:00:15           | 00:00:16         |                   |                 |                 |               |  
    | 00:00:10   | 00:00:10.500 |           |          | 00:00:03 | 00:00:06 | 01:00:00 | 01:00:10           | 01:00:10.500     |                   |                 | 00:00:03        | 00:00:06      |  
    |            |              | 00:00:10  | 00:00:20 | 00:00:05 | 00:00:07 | 00:00:01 |                    |                  | 00:00:11          | 00:00:21        | 00:00:05        | 00:00:07      |  
    |            |              |           |          | 01:00:00 | 01:00:01 | 00:00:01 |                    |                  |                   |                 | 01:00:01        | 01:00:02      |  
    |            |              |           | 00:00:20 |          | 00:00:10 | 00:00:15 |                    |                  |                   | 00:00:35        |                 | 00:00:10      |  
