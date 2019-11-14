Feature: EBU-TT-D lineHeight conversion

    On converting to EBU-TT-D, lineHeight values must be translated into percentages.

    Examples:
        | xml_file                     |
        | style_element_references.xml |

    Scenario: The value of tts:lineHeight shall be recalculated and expressed in percentage
        Given an xml file <xml_file>
        When it contains style "s1"
        And style "s1" has attribute "lineHeight" set to <lineHeight>
        And style "s1" has attribute "fontSize" set to <fontSize>
        And it contains some text with style "s1"
        When the document is generated
        And the EBU-TT-Live document is denested
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then the ebu_tt_d document contains style "autogenFontStyle_None_200.0" with attribute "lineHeight" set to <ebu_tt_d_value>

        Examples:
            | lineHeight | fontSize | ebu_tt_d_value |
            | 2c         | 2c       | 100%           |
            | 3c         | 2c       | 150%           |
            | 1c         | 2c       | 50%            |
            | 100%       | 2c       | 100%           |
            | 120%       | 2c       | 120%           |
            | 120.2%     | 2c       | 120.2%         |
            | 120.36%    | 2c       | 120.36%        |
            | 120.123%   | 2c       | 120.12%        |
            | normal     | 2c       | normal         |

