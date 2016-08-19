# SPEC-CONFORMANCE : R70
@validation @xsd @syntax @times
Feature: smpte datatype constraints

  # SPEC-CONFORMANCE: R45 R48 R51 (body begin, end and dur SMPTE)
  Scenario: Valid SMPTE timings on body 
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is valid

    Examples:
    | xml_file                | time_base | body_begin  | body_end       | body_dur     |
    | timeBase_timeformat.xml | smpte     | 00:00:00:00 |                |              
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12    |              |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12    | 11:11:11:11  |
    | timeBase_timeformat.xml | smpte     |             |                | 11:11:11:11  |

  Scenario: Invalid SMPTE timings on body
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is invalid

    Examples:
    | xml_file                | time_base | body_begin   | body_end | body_dur |  
    | timeBase_timeformat.xml | smpte     | 00:00:00     |          |          |  
    | timeBase_timeformat.xml | smpte     | 11           |          |          |  
    | timeBase_timeformat.xml | smpte     | 11:11.11     |          |          |  
    | timeBase_timeformat.xml | smpte     | 11.11.11     |          |          |  
    | timeBase_timeformat.xml | smpte     | 11.11:11     |          |          |  
    | timeBase_timeformat.xml | smpte     | 11.11        |          |          |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:111 |          |          |  


  # SPEC-CONFORMANCE: R54 R57 R (div begin and end  SMPTE)
  Scenario: Valid SMPTE timings on div 
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is valid

    Examples:
    | xml_file                | time_base | div_begin   | div_end     |  
    | timeBase_timeformat.xml | smpte     | 00:00:00:00 |             |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12 |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12 |  

  Scenario: Invalid SMPTE timings on div 
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is invalid

    Examples:
    | xml_file                | time_base | div_begin    | div_end |  
    | timeBase_timeformat.xml | smpte     | 00:00:00     |         |  
    | timeBase_timeformat.xml | smpte     | 11           |         |  
    | timeBase_timeformat.xml | smpte     | 11:11.11     |         |  
    | timeBase_timeformat.xml | smpte     | 11.11.11     |         |  
    | timeBase_timeformat.xml | smpte     | 11.11:11     |         |  
    | timeBase_timeformat.xml | smpte     | 11.11        |         |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:111 |         |  


  # SPEC-CONFORMANCE: R60 R63 (p begin and end SMPTE)
  Scenario: Valid SMPTE timings on p  
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is valid

    Examples:
    | xml_file                | time_base | p_begin     | p_end       |  
    | timeBase_timeformat.xml | smpte     | 00:00:00:00 |             |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12 |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12 |  
   
  Scenario: Inalid SMPTE timings on p 
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is invalid

    Examples:
    | xml_file                | time_base | p_begin      | p_end |  
    | timeBase_timeformat.xml | smpte     | 00:00:00     |       |  
    | timeBase_timeformat.xml | smpte     | 11           |       |  
    | timeBase_timeformat.xml | smpte     | 11:11.11     |       |  
    | timeBase_timeformat.xml | smpte     | 11.11.11     |       |  
    | timeBase_timeformat.xml | smpte     | 11.11:11     |       |  
    | timeBase_timeformat.xml | smpte     | 11.11        |       |  
    | timeBase_timeformat.xml | smpte     | 11:11:11:111 |       |  

