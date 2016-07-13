Feature: ttp:timeBase attribute is mandatory
  Every document shall declare ttp:timeBase

  Scenario: Invalid ttp:timeBase
        Given an xml file <xml_file>
        And it has ttp:timeBase attribute <time_base>
        Then document is invalid

        Examples:
        | xml_file                         | time_base      |
        | timeBase_attribute_mandatory.xml |                |
        | timeBase_attribute_mandatory.xml | *?Empty?*      |
        | timeBase_attribute_mandatory.xml | hello          |
        | timeBase_attribute_mandatory.xml | wrong timebase |

    Scenario: Valid Sequence head attributes
        Given an xml file <xml_file>
        And it has ttp:timeBase attribute <time_base>
        Then document is valid

        Examples:
        | xml_file                         | time_base |
        | timeBase_attribute_mandatory.xml | smpte     |
        | timeBase_attribute_mandatory.xml | clock     |
        | timeBase_attribute_mandatory.xml | media     |

