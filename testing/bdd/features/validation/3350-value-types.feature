
@validation @xsd @syntax @times
Feature: Value types from 3350

  # SPEC-CONFORMANCE: R93
  Scenario Outline: Valid colour values
    Given an xml file "3350_value_types.xml"
    When it has tts:color attribute with value <color>
    Then document is valid

    Examples:
    | color             |
    | white             |
    | rgb(0,0,0)      |
    | rgba(0,0,0,255)   |
    | #000000         |
    | #000000FF       |

  Scenario Outline: Invalid colour values
    Given an xml file "3350_value_types.xml"
    When it has tts:color attribute with value <color>
    Then document is invalid

    Examples:
    | color           |
    | pinkish-green   |
    | rgb(0,0,999)    |
    | rgba(0,0)       |
    | rgba(0,256,0,0) |
    | #00MM           |
    | 000000          |


  # SPEC-CONFORMANCE: R94
  Scenario: Valid extent values
    Given an xml file "3350_value_types.xml"
    When it has region extent attribute with value <extent>
    Then document is valid

    Examples:
    | extent  |
    | 1% 1%   |
    | 1c 1c   |
    | 1px 1px |

  Scenario: Invalid extent values
    Given an xml file "3350_value_types.xml"
    When it has region extent attribute with value <extent>
    Then document is invalid

    Examples:
    | extent |
    | 1 1    |
    | -1c 1c |
    | 1px    |

  # SPEC-CONFORMANCE: R95
  Scenario: Valid font size values
    Given an xml file "3350_value_types.xml"
    When it has tts:fontSize attribute with value <font_size>
    Then document is valid

    Examples:
    | font_size |
    | 1%  2%    |
    | 1.5px     |
    | 1c 0c     |
    | 1c  2c    |
    | +1px      |


  Scenario: Invalid font size values
    Given an xml file "3350_value_types.xml"
    When it has tts:fontSize attribute with value <font_size>
    Then document is invalid

    Examples:
    | font_size |
    | 1% 1% 1%  |
    | 1em       |
    | 1c1c      |
    | -1% 1%    |
    | 1%  2c    |


  # SPEC-CONFORMANCE: R97
  Scenario: Valid line padding values
    Given an xml file "3350_value_types.xml"
    When it has linePadding attribute with value <line_padding>
    Then document is valid

    Examples:
    | line_padding |
    | 1c           |
    | 0.5c         |
    | .5c         |

  Scenario: Invalid line padding values
    Given an xml file "3350_value_types.xml"
    When it has linePadding attribute with value <line_padding>
    Then document is invalid

    Examples:
    | line_padding |
    | 1%           |
    | 1px          |
    | -1c          |
    | 1em          |

  # SPEC-CONFORMANCE: R98
  Scenario: Valid line height values
    Given an xml file "3350_value_types.xml"
    When it has lineHeight attribute with value <line_height>
    Then document is valid

    Examples:
    | line_height |
    | normal      |
    | 1.5%        |
    | 1c          |
    | 1px         |

  Scenario: Invalid line height values
    Given an xml file "3350_value_types.xml"
    When it has lineHeight attribute with value <line_height>
    Then document is invalid

    Examples:
    | line_height |
    | hello       |
    | 1em         |
    | 1c 2c       |
    | -1px        |

  # SPEC-CONFORMANCE: R99
  Scenario: Valid origin values
    Given an xml file "3350_value_types.xml"
    When it has origin attribute with value <origin>
    Then document is valid

    Examples:
    | origin   |
    | 10% 10%  |
    | 1c 1c    |
    | 1px 1px  |
    | -1px 1px |
    | 1px -1px |

  Scenario: Invalid origin values
    Given an xml file "3350_value_types.xml"
    When it has origin attribute with value <origin>
    Then document is invalid

    Examples:
    | origin   |
    | 1em 1em  |
    | 1px1px   |
    | 1 1      |



