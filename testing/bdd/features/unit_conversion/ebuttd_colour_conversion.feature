Feature: EBU-TT-D colour conversion

    On converting to EBU-TT-D, colours must be translated into hex codes.

    Examples:
        | xml_file                     |
        | style_element_references.xml |

    Scenario: All colour values shall be converted to hex notated RGB colour triple
        Given an xml file <xml_file>
        When it contains style "s1"
        And style "s1" has attribute "color" set to <ebu_tt_live_value>
        And it contains some text with style "s1"
        When the document is generated
        And the EBU-TT-Live document is denested
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then the ebu_tt_d document contains style "s1" with attribute "color" set to <ebu_tt_d_value>

        Examples:
            | ebu_tt_live_value | ebu_tt_d_value |
            | transparent       | #00000000      |
            | black             | #000000ff      |
            | SILVER            | #c0c0c0ff      |
            | gray              | #808080ff      |
            | white             | #ffffffff      |
            | maroon            | #800000ff      |
            | red               | #ff0000ff      |
            | purple            | #800080ff      |
            | fuchsia           | #ff00ffff      |
            | magenta           | #ff00ffff      |
            | green             | #008000ff      |
            | lime              | #00ff00ff      |
            | olive             | #808000ff      |
            | yellow            | #ffff00ff      |
            | navy              | #000080ff      |
            | blue              | #0000ffff      |
            | teal              | #008080ff      |
            | aqua              | #00ffffff      |
            | cyan              | #00ffffff      |
            | #ffff00ff         | #ffff00ff      |
