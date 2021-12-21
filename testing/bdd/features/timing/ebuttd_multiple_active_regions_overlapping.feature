Feature: Multiple active regions overlapping


        Examples:
            | xml_file                       |
            | active_regions_overlapping.xml |


    Scenario: Multiple active regions that overlap the application shall exit with an error.

        Given an xml file <xml_file>
        When  it has region "r1"
        And   region "r1" has attribute "origin" set to <r1_origin>
        And   region "r1" has attribute "extent" set to <r1_extent>
        And   it has region "r2"
        And   region "r2" has attribute "origin" set to <r2_origin>
        And   region "r2" has attribute "extent" set to <r2_extent>
        And   it has p_element "p1"
        And   it has p_element "p2"
        And   p_element "p1" has attribute "region" set to "r1"
        And   p_element "p2" has attribute "region" set to "r2"
        And   p_element "p1" has attribute "begin" set to <p1_begin>
        And   p_element "p1" has attribute "end" set to <p1_end>
        And   p_element "p2" has attribute "begin" set to <p2_begin>
        And   p_element "p2" has attribute "end" set to <p2_end>
        When  the document is generated
        And   the EBU-TT-Live document is converted to a EBU-TT-D
        Then  application should exit with error OverlappingActiveElementsError

        Examples:
            | r1_origin     | r1_extent  | r2_origin  | r2_extent    | p1_begin     | p1_end       | p2_begin     | p2_end       |
            | 14.375% 50%   | 71.25% 45% | 30% 65%    | 50% 30%      | 12:24:25.860 | 12:26:25.860 | 12:25:25.860 | 12:30:25.860 |
            | 12.23% 20.15% | 85.25% 10% | 20% 15%    | 40% 15%      | 00:12:25.421 | 00:18:25.123 | 00:15:25.542 | 00:16:23.220 |
            | 9.23% 26.15%  | 75.25% 9%  | 70% 10%    | 14% 16%      | 00:12:25.421 | 00:18:25.123 | 00:15:25.542 | 00:16:23.220 |
            | 1.23%  12.15% | 40.25% 10% | 33.56% 15% | 10.23% 1.12% | 01:12:25.421 | 01:18:25.123 | 01:15:25.542 | 01:16:23.220 |

    Scenario: Regions extending outside the root container region

        Given an xml file <xml_file>
        When  it has region "r1"
        And   region "r1" has attribute "origin" set to <r1_origin>
        And   region "r1" has attribute "extent" set to <r1_extent>
        And   it has p_element "p1"
        And   p_element "p1" has attribute "region" set to "r1"
        And   the document is generated
        When  the EBU-TT-Live document is converted to a EBU-TT-D
        Then  application should exit with error RegionExtendingOutsideDocumentError

        Examples:
            | r1_origin  | r1_extent  |
            | -1% 50%    | 71.25% 45% |
            | 40% 50%    | 71.25% 45% |
            | 400% -5%   | 71.25% 45% |
            | 40% 29.85% | 45% 71.25% |
