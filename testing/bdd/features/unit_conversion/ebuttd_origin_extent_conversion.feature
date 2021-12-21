Feature: EBU-TT-D origin and extent conversion

    On converting to EBU-TT-D, origin and extent values must be translated into percentages
    based on the cellResolution field on the tt element.

    Examples:
        | xml_file                     |
        | style_element_references.xml |

    Scenario: convert values of tts:origin and tts:extent attributes on regions to percent units from cell units
        Given an xml file <xml_file>
        When the document has a cell resolution of "32 15"
        And it contains region "r1"
        And region "r1" has attribute "origin" set to "10c 10c"
        And region "r1" has attribute "extent" set to "14c 4c"
        And it contains some text with region "r1"
        When the document is generated
        And the EBU-TT-Live document is denested
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then the ebu_tt_d document contains region "r1" with attribute "origin" set to "31.25% 66.67%"
        And the ebu_tt_d document contains region "r1" with attribute "extent" set to "43.75% 26.67%"

    Scenario: convert values of tts:origin and tts:extent attributes on regions to percent units from pixel units
        Given an xml file <xml_file>
        When the document has an extent of "640px 480px"
        And it contains region "r1"
        And region "r1" has attribute "origin" set to "200px 360px"
        And region "r1" has attribute "extent" set to "220px 100px"
        And it contains some text with region "r1"
        When the document is generated
        And the EBU-TT-Live document is denested
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then the ebu_tt_d document contains region "r1" with attribute "origin" set to "31.25% 75.0%"
        And the ebu_tt_d document contains region "r1" with attribute "extent" set to "34.38% 20.83%"
