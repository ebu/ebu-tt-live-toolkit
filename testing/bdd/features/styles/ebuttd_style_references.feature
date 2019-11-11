@styles @document @ebuttd_conversion 
Feature: Remove style elements that refer to other style elements

  Examples:
    | xml_file                     |
    | style_element_references.xml |


  Scenario: Convert style element with reference to another style to a presentationally equivalent one
    Given an xml file <xml_file>
    When  it contains style "s_default"
    And   style "s_default" has attribute "color" set to "white"
    And   style "s_default" has attribute "backgroundColor" set to "black"
    And   it contains style "s_font_reith"
    And   style "s_font_reith" has attribute "style" set to "s_default"
    And   style "s_font_reith" has attribute "fontFamily" set to "reith"
    And   it contains style "s_font_monospace"
    And   style "s_font_monospace" has attribute "fontFamily" set to "monospace"
    And   it contains style "s_top"
    And   style "s_top" has attribute "style" set to "s_font_reith s_font_monospace"
    And   style "s_top" has attribute "color" set to "yellow"
    And   it contains some text with style "s_top"
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  the ebu_tt_d document contains style "s_top" with attribute "fontFamily" set to "monospace"
    And   the ebu_tt_d document contains style "s_top" with attribute "color" set to "#ffff00ff"
    And   the ebu_tt_d document contains style "s_top" with attribute "backgroundColor" set to "#000000ff"


  Scenario: Convert padding specifed on style applied to region to padding specified only on region when padding is on both style and region
    Given an xml file <xml_file>
    When  the document has an extent of "100px 100px"
    And   it contains style "s1"
    And   style "s1" has attribute "padding" set to "10px"
    And   it contains region "r1"
    And   region "r1" has attribute "style" set to "s1"
    And   region "r1" has attribute "padding" set to "5px"
    And   it contains some text with region "r1"
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   the ebu_tt_d document contains style "s1" without a "padding" attribute
    And   the ebu_tt_d document contains region "r1" with attribute "padding" set to "5px"


  Scenario: Convert padding specifed on style applied to region to padding specified only on region when padding is only on style
    Given an xml file <xml_file>
    When  the document has an extent of "100px 100px"
    And   it contains style "s1"
    And   style "s1" has attribute "padding" set to "10px"
    And   it contains region "r1"
    And   region "r1" has attribute "style" set to "s1"
    And   it contains some text with region "r1"
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   the ebu_tt_d document contains style "s1" without a "padding" attribute
    And   the ebu_tt_d document contains region "r1" with attribute "padding" set to "10px"


  Scenario: Convert padding specifed on 2 styles applied to a region to padding specified only on region when padding is only on style
    Given an xml file <xml_file>
    When  the document has an extent of "100px 100px"
    And   it contains style "s1"
    And   style "s1" has attribute "padding" set to "10px"
    When  it contains style "s2"
    And   style "s2" has attribute "padding" set to "5px"
    And   it contains region "r1"
    And   region "r1" has attribute "style" set to "s1 s2"
    And   it contains some text with region "r1"
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   the ebu_tt_d document contains region "r1" with attribute "padding" set to "5px"


  Scenario: Convert padding specifed on 2 styles where one inherits from another applied to a region to padding specified only on region when padding is only on style
    Given an xml file <xml_file>
    When  the document has an extent of "100px 100px"
    And   it contains style "s1"
    And   style "s1" has attribute "padding" set to "10px"
    When  it contains style "s2"
    And   style "s2" has attribute "padding" set to "5px"
    When  it contains style "s3"
    And   style "s3" has attribute "color" set to "white"
    And   style "s3" has attribute "style" set to "s2"
    And   it contains region "r1"
    And   region "r1" has attribute "style" set to "s1 s3"
    And   it contains some text with region "r1"
    When  the document is generated
    And   the EBU-TT-Live document is denested
    And   the EBU-TT-Live document is converted to EBU-TT-D
    Then  EBUTTD document is valid
    And   the ebu_tt_d document contains region "r1" with attribute "padding" set to "5px"
