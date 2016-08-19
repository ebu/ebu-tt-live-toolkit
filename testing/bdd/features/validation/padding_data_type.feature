@validation @syntax
Feature: Padding Element and Datatype testing
  tts:padding is only allowed on certain elements. values are constrained to one, two, three or four non-negative numbers appended by percentage “%”, c” or “px”, delimited by a space.

  ## Assumes that we can pass <tag> to the examples so that we test that the attribute is only applied to the elements that support it.
  ## If we can't, this restriction will be built into the template.
  Scenario: Valid padding on element
    Given an xml file <xml_file>
    When <tag> has a padding attribute
    Then document is valid

    Examples:
    | xml_file              | tag       |
    | padding_data_type.xml | tt:style  |
    | padding_data_type.xml | tt:region |

  Scenario: Invalid padding on element
    Given an xml file <xml_file>
    When <tag> has a padding attribute
    Then document is invalid

    Examples:
    | xml_file              | tag     |
    | padding_data_type.xml | tt:p    |
    | padding_data_type.xml | tt:span |


  ## SPEC-CONFORMANCE: R100
  ## Assumes something like this in the template: <tag tts:padding="{{value1}} {{value2}} {{value3}} {{value4}}">
  ## Note that this attribute can have 1, 2, 3, or 4 values
  Scenario: Valid padding datatype
    Given an xml file <xml_file>
    When it has a padding attribute
    And the padding attribute has <value1>
    And the padding attribute has <value2>
    And the padding attribute has <value3>
    And the padding attribute has <value4>
    Then document is valid

    Examples:
    | xml_file              | value1 | value2  | value3 | value4 |
    | padding_data_type.xml | 1px    |         |        |        |
    | padding_data_type.xml | +1px   |         |        |        |
    | padding_data_type.xml | -1px   |         |        |        |
    | padding_data_type.xml | -.5px  |         |        |        |
    | padding_data_type.xml | 001px  |         |        |        |
    | padding_data_type.xml | 1px    | 1c      |        |        |
    | padding_data_type.xml | 1px    | 1c      | 1%     |        |
    | padding_data_type.xml | 1px    | 1c      | 1%     | 1px    |
    | padding_data_type.xml | 1.5px  | 1.3333% | 1.5px  | 0.05px |
    | padding_data_type.xml | 1px    | 1c      | 0px    | 0px    |
    | padding_data_type.xml | 1px    | 001c    | 0px    | 0px    |

  Scenario: Invalid padding datatype
    Given an xml file <xml_file>
    When it has a padding attribute
    And the padding attribute has <value1>
    And the padding attribute has <value2>
    And the padding attribute has <value3>
    And the padding attribute has <value4>
    Then document is invalid

    Examples:
    | xml_file              | value1 | value2 | value3 | value4 |
    | padding_data_type.xml | 1      |        |        |        |
    | padding_data_type.xml | 1em    |        |        |        |
    | padding_data_type.xml | --1px  |        |        |        |
    | padding_data_type.xml |        |        |        |        |
    | padding_data_type.xml | ' '    |        |        |        |
    | padding_data_type.xml |        |        |        |        |
