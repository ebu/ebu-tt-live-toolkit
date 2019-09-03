Feature: Merging nested elements


    Scenario: If a div contains no tt:p elements it is discarded
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And  divs with no p elements are removed

        Examples:
            | xml_file                              |
            | nested_elements_hardcoded_no_divs.xml |

    Scenario: No div should contain any other divs
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And no div contains any other divs

        Examples:
            | xml_file                      |
            | nested_elements_hardcoded.xml |