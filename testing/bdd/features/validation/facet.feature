@validation @syntax @sequence @xsd
Feature: Facet
  Rules on use of ebuttm:facet and ebuttm:documentFacet


  # SPEC-CONFORMANCE: R26 R66 R67
  # skipped because the semantic validation does not check facets yet
  @skip
  Scenario: Invalid term identifier
    Given an xml file <xml_file>
    When it has facet1 applied to element <parent1>
    And facet1 has attribute <link1>
    And facet1 contains string <term1>
    And it has facet2 applied to element <parent2>
    And facet2 has attribute <link2>
    And facet2 contains string <term2>
    Then document is invalid

    Examples:
    | xml_file  | parent1 | link1            | term1   | parent2 | link2            | term2   |
    | facet.xml | body    | http://link1.com | string1 | body    | http://link1.com | string1 |


  Scenario: Valid term identifier
    Given an xml file <xml_file>
    When it has facet1 applied to element <parent1>
    And facet1 has attribute <link1>
    And facet1 contains string <term1>
    And it has facet2 applied to element <parent2>
    And facet2 has attribute <link2>
    And facet2 contains string <term2>
    Then document is valid

    Examples:
    | xml_file  | parent1  | link1            | term1   | parent2  | link2            | term2   |
    | facet.xml | body     | http://link1.com | string1 | div      | http://link1.com | string1 |
    | facet.xml | p        | http://link1.com | string1 | p        | http://link2.com | string2 |
    | facet.xml | span     | http://link1.com | string1 | span     | http://link1.com | string2 |


  # SPEC-CONFORMANCE: R27 R28 R29 R30
  Scenario: Valid Facet Summary
    Given an xml file <xml_file>
    When it has element facet1 with attribute <expresses1>
    And it has element facet2 with attribute <expresses2>
    And it has element facet3 with attribute <expresses3>
    And documentFacet has atribute <summary>
    Then document is valid

    Examples:
    | xml_file  | expresses1 | expresses2 | expresses3 | summary     |
    | facet.xml | has        | has        | has        | all_has     |
    | facet.xml | has_not    | has_not    | has_not    | all_has_not |
    | facet.xml | has        | has_not    | has        | mixed       |
    | facet.xml | unknown    | has        | has        | mixed       |
    | facet.xml |            |            |            | unspecified |
    | facet.xml | unknown    | unknown    | unknown    | unspecified |


  Scenario: Invalid Facet Summary
    Given an xml file <xml_file>
    When it has element facet1 with attribute <expresses1>
    And it has element facet2 with attribute <expresses2>
    And it has element facet3 with attribute <expresses3>
    And documentFacet has atribute <summary>
    Then document is invalid

    Examples:
    | xml_file  | expresses1 | expresses2 | expresses3 | summary     |
    | facet.xml | has_not    | has_not    | has_not    | has         |
    | facet.xml | has        | has_not    | has        | has         |
    | facet.xml |            |            |            | has_not     |
    | facet.xml | unknown    | unknown    | unknown    | has         |
    @skip # again semantic validation for that part is missing in the xml validation for now
    | facet.xml | has        | has        | has        | all_has_not |
    | facet.xml | unknown    | has        | has        | unspecified |
