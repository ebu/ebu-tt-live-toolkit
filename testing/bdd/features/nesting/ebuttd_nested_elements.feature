Feature: Merging nested elements


    Scenario: If a div contains no tt:p elements it is discarded
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And divs with no p elements are removed

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

    Scenario: When the P region matches the div region, remove p region
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And the p does not have a region attribute

        Examples:
            | xml_file                                |
            | p_regions_nested_elements_hardcoded.xml |

    Scenario: When the P region does not match the div region, remove p
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And the p has been removed from the div

        Examples:
            | xml_file                                |
            | p_regions_nested_elements_hardcoded.xml |

    Scenario: When the div has a Region but the P does not, change nothing
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And the div and p regions remain the same

        Examples:
            | xml_file                                |
            | p_regions_nested_elements_hardcoded.xml |

    Scenario: No span should contain any other span
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And no span contains any other spans

        Examples:
            | xml_file                   |
            | nested_spans_hardcoded.xml |

    Scenario: Nested spans with styles should create new, combined styles
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And the second span's style is outerinnerYellow

        Examples:
            | xml_file                   |
            | nested_spans_hardcoded.xml |

    Scenario: New styles are not created where the values of the new style match an existing one
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And there is no style named "nestnest"

        Examples:
            | xml_file                   |
            | nested_spans_hardcoded.xml |

    Scenario: Nested styles with percentage sizes are correctly calculated
        Given an xml file <xml_file>
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then EBUTTD document is valid
        And any span with the style "nestSizing" also has the style "autogenFontStyle_None_50.0"
        And any span with the style "nestSizingnestSizing" also has the style "autogenFontStyle_None_25.0"
        And any span with the style "nestSizingnestSizingnestSizing" also has the style "autogenFontStyle_None_12.5"

        Examples:
            | xml_file                   |
            | nested_spans_hardcoded.xml |