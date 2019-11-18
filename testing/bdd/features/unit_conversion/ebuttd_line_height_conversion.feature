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
        Then the ebu_tt_d document contains style <style_id> with attribute "lineHeight" set to <ebu_tt_d_value>

        Examples:
            | lineHeight | fontSize | style_id                           | ebu_tt_d_value |
            | 2c         | 2c       | autogenFontStyle_None_200.0_100.0  | 100%           |
            | 3c         | 2c       | autogenFontStyle_None_200.0_150.0  | 150%           |
            | 1c         | 2c       | autogenFontStyle_None_200.0_50.0   | 50%            |
            | 100%       | 2c       | autogenFontStyle_None_200.0_100.0  | 100%           |
            | 120%       | 2c       | autogenFontStyle_None_200.0_120.0  | 120%           |
            | 120.2%     | 2c       | autogenFontStyle_None_200.0_120.2  | 120.2%         |
            | 120.36%    | 2c       | autogenFontStyle_None_200.0_120.36 | 120.36%        |
            | 120.123%   | 2c       | autogenFontStyle_None_200.0_120.12 | 120.12%        |
            | normal     | 2c       | autogenFontStyle_None_200.0_n      | normal         |

