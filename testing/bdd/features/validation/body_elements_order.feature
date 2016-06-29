Feature: Body Elements Constraints testing
    The body elements have to respect some order

    Scenario: Invalid body elements layout
        Given a xml file <xml_file>
        And its body has a <body_element>
        Then document is invalid

        Examples:
        | xml_file                | body_element |
        | body_elements_order.xml | span         |
        | body_elements_order.xml | p            |
        | body_elements_order.xml | br           |
