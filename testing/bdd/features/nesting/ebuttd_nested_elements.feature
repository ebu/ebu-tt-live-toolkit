Feature: Merging nested elements


Scenario: If a tt:div in the input contains no tt: p elements, the div and its contents shall be discarded
Given an xml file <xml_file>
When it contains a div with id "d1"
And it contains a div with id "d2"
And it has p_element "p1"
And div "d1" has element "p1"
When the document is generated
And the EBU-TT-Live document is converted to EBU-TT-D
Then EBUTTD document is valid
# Then the div and its contents shall be discarded

Examples:
| xml_file            |
| nested_elements.xml |

Scenario: If a div contains no divs and no tt:p elements it is discarded
Given an xml file <xml_file>
When it contains a div with id "d1"
And it contains a div with id "d2"
#And div "d1" contains div "d1a"
#And div "d2" contains div "d2a"
And it has p_element "p1"
And div "d2" has element "p1"
When the document is generated
And the EBU-TT-Live document is converted to EBU-TT-D
Then EBUTTD document is valid

Examples:
| xml_file            |
| nested_elements.xml |