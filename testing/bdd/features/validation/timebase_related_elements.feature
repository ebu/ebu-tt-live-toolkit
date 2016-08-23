@validation @syntax @sequence @xsd
Feature: Timebase related elements
  Timebase-dependent elements and their values



  # SPEC-CONFORMANCE: R72
  Scenario: Valid markerMode
    Given an xml file <xml_file>
    When it has tt:timebase with the value <timebase>
    And it has ttp:markerMode value <markerMode>
    Then document is valid

    Examples:
    | xml_file              | timebase | markerMode    |  
    | timebase_elements.xml | smpte    | continuous    |  
    | timebase_elements.xml | smpte    | discontinuous |  

  Scenario: Invalid markerMode
    Given an xml file <xml_file>
    When it has tt:timebase with the value <timebase>
    And it has ttp:markerMode value <markerMode>
    Then document is invalid

    Examples:
    | xml_file              | timebase | markerMode |  
    | timebase_elements.xml | smpte    |            |  
    | timebase_elements.xml | smpte    | hello      |  
    | timebase_elements.xml | smpte    | 1          | 


  # SPEC-CONFORMANCE: R73a
  Scenario: Valid dropMode
    Given an xml file <xml_file>
    When it has tt:timebase with the value <timebase>
    And it has ttp:frameRate 
    And it has ttp:frameRateMultiplier
    And the calculation of the frame rate from ttp:frameRate and ttp:frameRateMultiplier results in <effectiveFrameRate>
    And the it has tt:dropMode value <dropMode> 
    Then document is valid

    Examples:
    | xml_file              | timebase | effectiveFrameRate | dropMode |  
    | timebase_elements.xml | smpte    | 1                  | nonDrop  |  
    | timebase_elements.xml | smpte    | 1.1                | dropPAL  |  
    | timebase_elements.xml | smpte    | 1.1                | dropNTSC |  

  Scenario: Invalid dropMode
    Given an xml file <xml_file>
    When it has tt:timebase with the value <timebase>
    And it has ttp:frameRate 
    And it has ttp:frameRateMultiplier
    And the calculation of the frame rate from ttp:frameRate and ttp:frameRateMultiplier results in <effectiveFrameRate>
    And the it has tt:dropMode value <dropMode> 
    Then document is invalid

    Examples:
    | xml_file              | timebase | effectiveFrameRate | dropMode |  
    | timebase_elements.xml | smpte    | 1.1                | nonDrop  |  
    | timebase_elements.xml | smpte    | 1                  | dropPAL  |  
    | timebase_elements.xml | smpte    | 1                  | dropNTSC |  
