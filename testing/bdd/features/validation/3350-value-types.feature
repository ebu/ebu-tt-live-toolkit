
@validation @xsd @syntax @times
Feature: Value types from 3350

  # SPEC-CONFORMANCE: R93
  Scenario: Valid colour values
    Given an xml file <xml_file>
    When it has tts:color attribute with value <color> 
    Then document is valid

    Examples:
    | xml_file             | color           |  
    | 3350_value_types.xml | white           |  
    | 3350_value_types.xml | rgb(0,0,0)      |  
    | 3350_value_types.xml | rgba(0,0,0,255) |  
    | 3350_value_types.xml | #000000         |  
    | 3350_value_types.xml | #000000FF       |  

  Scenario: Invalid colour values
    Given an xml file <xml_file>
    When it has tts:color attribute with value <color> 
    Then document is valid

    Examples:
    | xml_file             | color         |  
    | 3350_value_types.xml | pinkish-green |  
    | 3350_value_types.xml | rgb(0,0,999)  |  
    | 3350_value_types.xml | rgba(0,0)     |  
    | 3350_value_types.xml | #00MM         |  
    | 3350_value_types.xml | 000000        |  


  # SPEC-CONFORMANCE: R94
  Scenario: Valid extent values
    Given an xml file <xml_file>
    When it has extent attribute with value <extent> 
    Then document is valid

    Examples:
    | xml_file             | extent |  
    | 3350_value_types.xml | 1%     |  
    | 3350_value_types.xml | 1c     |  
    | 3350_value_types.xml | 1px    |  

  Scenario: Invalid extent values
    Given an xml file <xml_file>
    When it has extent attribute with value <extent> 
    Then document is invalid

    Examples:
    | xml_file             | extent |  
    | 3350_value_types.xml | 1      |  
    | 3350_value_types.xml | -1c    |  
    | 3350_value_types.xml | 1px    |  

  # SPEC-CONFORMANCE: R95
  Scenario: Valid font size values
    Given an xml file <xml_file>
    When it has tts:fontSize attribute with value <fontSize> 
    Then document is valid

    Examples:
    | xml_file             | fontSize |  
    | 3350_value_types.xml | 1%  2c   |  
    | 3350_value_types.xml | 1.5px     |  
    | 3350_value_types.xml | 1c 0c    |  
    | 3350_value_types.xml | -1%  2c   |  
    | 3350_value_types.xml | +1px     |  


  Scenario: Invalid font size values
    Given an xml file <xml_file>
    When it has tts:fontSize attribute with value <fontSize> 
    Then document is invalid

    Examples:
    | xml_file             | fontSize |  
    | 3350_value_types.xml | 1% 1% 1% |  
    | 3350_value_types.xml | 1em      |  
    | 3350_value_types.xml | 1c1c     |  

 # SPEC-CONFORMANCE: R96
  Scenario: Valid frame rate multiplier values
    Given an xml file <xml_file>
    When it has frameRateMultiplier attribute with value <frameRateMultiplier> 
    Then document is valid

    Examples:
    | xml_file             | frameRateMultiplier |  
    | 3350_value_types.xml | 1 1                 |  
    | 3350_value_types.xml | 010 010             |  

  Scenario: Invalid frame rate multiplier values
    Given an xml file <xml_file>
    When it has frameRateMultiplier attribute with value <frameRateMultiplier> 
    Then document is invalid

    Examples:
   | xml_file             | frameRateMultiplier |  
   | 3350_value_types.xml | 1                   |  
   | 3350_value_types.xml | 000 010             |  
   | 3350_value_types.xml | 1.5 1               |  
   | 3350_value_types.xml | -1 1                |  
   | 3350_value_types.xml | 1px 1px             |  

  # SPEC-CONFORMANCE: R97
  Scenario: Valid line padding values
    Given an xml file <xml_file>
    When it has linePadding attribute with value <linePadding> 
    Then document is valid

    Examples:
    | xml_file             | linePadding |  
    | 3350_value_types.xml | 1c                 |  
    | 3350_value_types.xml | 0.5c             |  
    | 3350_value_types.xml | +.5c             |  

  Scenario: Invalid line padding values
    Given an xml file <xml_file>
    When it has linePadding attribute with value <linePadding> 
    Then document is invalid

    Examples:
    | xml_file             | linePadding |  
    | 3350_value_types.xml | 1%          |  
    | 3350_value_types.xml | 1px         |  
    | 3350_value_types.xml | -1c         |  
    | 3350_value_types.xml | 1em         |  

  # SPEC-CONFORMANCE: R98
  Scenario: Valid line height values
    Given an xml file <xml_file>
    When it has lineHeight attribute with value <lineHeight> 
    Then document is valid

    Examples:
    | xml_file             | lineHeight |  
    | 3350_value_types.xml | normal     |  
    | 3350_value_types.xml | 1.5%       |  
    | 3350_value_types.xml | 1c         |  
    | 3350_value_types.xml | 1px        |  

  Scenario: Invalid line height values
    Given an xml file <xml_file>
    When it has lineHeight attribute with value <lineHeight> 
    Then document is invalid

    Examples:
    | xml_file             | lineHeight |  
    | 3350_value_types.xml | hello      |  
    | 3350_value_types.xml | 1em        |  
    | 3350_value_types.xml | 1c 2c      |  
    | 3350_value_types.xml | -1c        |  

  # SPEC-CONFORMANCE: R99
  Scenario: Valid origin values
    Given an xml file <xml_file>
    When it has origin attribute with value <origin> 
    Then document is valid

    Examples:
    | xml_file             | origin  |  
    | 3350_value_types.xml | 10% 10% |  
    | 3350_value_types.xml | 1c 1c   |  
    | 3350_value_types.xml | 1px 1px |  

  Scenario: Invalid origin values
    Given an xml file <xml_file>
    When it has origin attribute with value <origin> 
    Then document is invalid

    Examples:
    | xml_file             | origin   |  
    | 3350_value_types.xml | -10% 10% |  
    | 3350_value_types.xml | 1em 1em  |  
    | 3350_value_types.xml | 1px1px   |  
    | 3350_value_types.xml | 1 1      |  



