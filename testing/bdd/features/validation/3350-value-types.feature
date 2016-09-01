
@validation @xsd @syntax @times
Feature: Value types from 3350

  # SPEC-CONFORMANCE: R93
  Scenario: Valid colour values
    Given an xml file <xml_file>
    When it has tts:color attribute with value <color>
    Then document is valid

    Examples:
    | xml_file             | color           |
    | 3350_value_types.xml | white           |
    | 3350_value_types.xml | rgb(0,0,0)      |
    | 3350_value_types.xml | rgba(0,0,0,255) |
    | 3350_value_types.xml | #000000         |
    | 3350_value_types.xml | #000000FF       |

  Scenario: Invalid colour values
    Given an xml file <xml_file>
    When it has tts:color attribute with value <color>
    Then document is invalid

    Examples:
    | xml_file             | color           |
    | 3350_value_types.xml | pinkish-green   |
    | 3350_value_types.xml | rgb(0,0,999)    |
    | 3350_value_types.xml | rgba(0,0)       |
    | 3350_value_types.xml | rgba(0,256,0,0) |
    | 3350_value_types.xml | #00MM           |
    | 3350_value_types.xml | 000000          |


  # SPEC-CONFORMANCE: R94
  Scenario: Valid extent values
    Given an xml file <xml_file>
    When it has region extent attribute with value <extent>
    Then document is valid

    Examples:
    | xml_file             | extent  |
    | 3350_value_types.xml | 1% 1%   |
    | 3350_value_types.xml | 1c 1c   |
    | 3350_value_types.xml | 1px 1px |

  Scenario: Invalid extent values
    Given an xml file <xml_file>
    When it has region extent attribute with value <extent>
    Then document is invalid

    Examples:
    | xml_file             | extent |
    | 3350_value_types.xml | 1 1    |
    | 3350_value_types.xml | -1c 1c |
    | 3350_value_types.xml | 1px    |

  # SPEC-CONFORMANCE: R95
  Scenario: Valid font size values
    Given an xml file <xml_file>
    When it has tts:fontSize attribute with value <font_size>
    Then document is valid

    Examples:
    | xml_file             | font_size |
    | 3350_value_types.xml | 1%  2%    |
    | 3350_value_types.xml | 1.5px     |
    | 3350_value_types.xml | 1c 0c     |
    | 3350_value_types.xml | 1c  2c    |
    | 3350_value_types.xml | +1px      |


  Scenario: Invalid font size values
    Given an xml file <xml_file>
    When it has tts:fontSize attribute with value <font_size>
    Then document is invalid

    Examples:
    | xml_file             | font_size |
    | 3350_value_types.xml | 1% 1% 1%  |
    | 3350_value_types.xml | 1em       |
    | 3350_value_types.xml | 1c1c      |
    | 3350_value_types.xml | -1% 1%    |
    | 3350_value_types.xml | 1%  2c    |


  # SPEC-CONFORMANCE: R97
  Scenario: Valid line padding values
    Given an xml file <xml_file>
    When it has linePadding attribute with value <line_padding>
    Then document is valid

    Examples:
    | xml_file             | line_padding |
    | 3350_value_types.xml | 1c           |
    | 3350_value_types.xml | 0.5c         |
    | 3350_value_types.xml | .5c         |

  Scenario: Invalid line padding values
    Given an xml file <xml_file>
    When it has linePadding attribute with value <line_padding>
    Then document is invalid

    Examples:
    | xml_file             | line_padding |
    | 3350_value_types.xml | 1%           |
    | 3350_value_types.xml | 1px          |
    | 3350_value_types.xml | -1c          |
    | 3350_value_types.xml | 1em          |

  # SPEC-CONFORMANCE: R98
  Scenario: Valid line height values
    Given an xml file <xml_file>
    When it has lineHeight attribute with value <line_height>
    Then document is valid

    Examples:
    | xml_file             | line_height |
    | 3350_value_types.xml | normal      |
    | 3350_value_types.xml | 1.5%        |
    | 3350_value_types.xml | 1c          |
    | 3350_value_types.xml | 1px         |

  Scenario: Invalid line height values
    Given an xml file <xml_file>
    When it has lineHeight attribute with value <line_height>
    Then document is invalid

    Examples:
    | xml_file             | line_height |
    | 3350_value_types.xml | hello       |
    | 3350_value_types.xml | 1em         |
    | 3350_value_types.xml | 1c 2c       |
    | 3350_value_types.xml | -1px        |

  # SPEC-CONFORMANCE: R99
  Scenario: Valid origin values
    Given an xml file <xml_file>
    When it has origin attribute with value <origin>
    Then document is valid

    Examples:
    | xml_file             | origin   |
    | 3350_value_types.xml | 10% 10%  |
    | 3350_value_types.xml | 1c 1c    |
    | 3350_value_types.xml | 1px 1px  |
    | 3350_value_types.xml | -1px 1px |
    | 3350_value_types.xml | 1px -1px |

  Scenario: Invalid origin values
    Given an xml file <xml_file>
    When it has origin attribute with value <origin>
    Then document is invalid

    Examples:
    | xml_file             | origin   |
    | 3350_value_types.xml | 1em 1em  |
    | 3350_value_types.xml | 1px1px   |
    | 3350_value_types.xml | 1 1      |



