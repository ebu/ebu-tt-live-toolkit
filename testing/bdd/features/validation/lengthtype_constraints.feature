Feature: EBU-TT lengthType validation

    If pixel units are used in style attributes on regions or styles but 'extent' has not been specified on the tt:tt element, the document is invalid.

    Examples:
        | xml_file                     |
        | style_element_references.xml |

    Scenario: throw an error and stop the processing if no pixel value for tts:extent is supplied on the tt:tt element but a region requires one
        Given an xml file <xml_file>
        When the document does not specify an extent
        And it contains region "r1"
        And region "r1" has attribute <attribute> set to <value>
        And it contains some text with region "r1"
        Then document has an ExtentMissingError

        Examples:
            | attribute    | value       |
            | origin       | 200px 360px |
            | extent       | 200px 360px |
            | padding      | 1px         |


    Scenario: throw an error and stop the processing if no pixel value for tts:extent is supplied on the tt:tt element but a style requires one
        Given an xml file <xml_file>
        When the document does not specify an extent
        And it contains style "s1"
        And style "s1" has attribute <attribute> set to <ebu_tt_live_value>
        And it contains some text with style "s1"
        Then document has an ExtentMissingError

        Examples:
            | attribute  | ebu_tt_live_value |
            | fontSize   | 20px              |
            | lineHeight | 25px              |
            | padding    | 1px               |
