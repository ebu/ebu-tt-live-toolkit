#  The Handover Manager may include the parameters ebuttp:authorsGroupIdentifier, ebuttp:authorsGroupControlToken and ebuttm:authorsGroupControlRequest from the currently selected input sequence within its output sequence. 

Feature: Include handover paramters in output    

  Examples:
  | xml_file     |  
  | handover.xml |  


  Scenario: Include current sequence handover parameters in output
    Given a test sequence
    And an xml file <xml_file>
    And it has <authorsGroupIdentifier1>
    And it has <authorsGroupControlToken1>
    And it has <authorsGroupControlRequest1>
    And the file is added to the sequence
    When the file is output
    Then the document has <authorsGroupIdentifier2>
    And it has <authorsGroupControlToken2>
    And it has <authorsGroupControlRequest2>

    Examples:
    | authorsGroupIdentifier1 | authorsGroupControlToken1 | authorsGroupControlRequest1 | authorsGroupIdentifier2 | authorsGroupControlToken2 | authorsGroupControlRequest2 |  
    | id1                     | 1                         | UseMe                       | id1                     | 1                         | UseMe                       |  
    # If control token value is unspecified, the handover node does not make its initial value explicit   
    | id1                     |                           |                             | id1                     |                           |                             |  

