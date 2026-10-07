@validation @syntax
Feature: Padding Element and Datatype testing
  tts:padding is only allowed on certain elements. values are constrained to one, two, three or four non-negative numbers appended by percentage “%”, c” or “px”, delimited by a space.

  ## Assumes that we can pass <tag> to the examples so that we test that the attribute is only applied to the elements that support it.
  ## If we can't, this restriction will be built into the template.
  Scenario Outline: Valid padding on element
    Given an xml file "padding_data_type.xml"
    When <tag> has a padding attribute
    Then document is valid

    Examples:
    | tag       |
    | tt:style  |
    | tt:region |

  Scenario Outline: Invalid padding on element
    Given an xml file "padding_data_type.xml"
    When <tag> has a padding attribute
    Then document is invalid

    Examples:
    | tag     |
    | tt:p    |
    | tt:span |


  ## SPEC-CONFORMANCE: R100
  ## Assumes something like this in the template: <tag tts:padding="{{value1}} {{value2}} {{value3}} {{value4}}">
  ## Note that this attribute can have 1, 2, 3, or 4 values
  Scenario Outline: Valid padding datatype
    Given an xml file "padding_data_type.xml"
    When it has a padding attribute
    And the padding attribute component 1 is <value1>
    And the padding attribute component 2 is <value2>
    And the padding attribute component 3 is <value3>
    And the padding attribute component 4 is <value4>
    Then document is valid

    Examples:
    | value1 | value2  | value3 | value4 |
    | 1px    |         |        |        |
    | +1px   |         |        |        |
    | -1px   |         |        |        |
    | -.5px  |         |        |        |
    | 001px  |         |        |        |
    | 1px    | 1c      |        |        |
    | 1px    | 1c      | 1%     |        |
    | 1px    | 1c      | 1%     | 1px    |
    | 1.5px  | 1.3333% | 1.5px  | 0.05px |
    | 1px    | 1c      | 0px    | 0px    |
    | 1px    | 001c    | 0px    | 0px    |

  Scenario Outline: Invalid padding datatype
    Given an xml file "padding_data_type.xml"
    When it has a padding attribute
    And the padding attribute component 1 is <value1>
    And the padding attribute component 2 is <value2>
    And the padding attribute component 3 is <value3>
    And the padding attribute component 4 is <value4>
    Then document is invalid

    Examples:
    | value1 | value2 | value3 | value4 |
    | 1      |        |        |        |
    | 1em    |        |        |        |
    | --1px  |        |        |        |
    |        |        |        |        |
    | ' '    |        |        |        |
    |        |        |        |        |
