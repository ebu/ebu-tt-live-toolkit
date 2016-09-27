@styles @document
Feature: Compute fontSize on a single EBU-TT Live element
 
# TODO: paddding, reference chain

  Scenario: Simple inheritance
    Given an EBU-TT Live document <xml_file>
    And the document has a cell resolution of <cell_resolution>
    And the document contains a region with applied font size <region_size> 
    And the document contains a div with applied font size <div_size> that references the region
    And the div has a child p with applied font size <p_size>
    And the p has a child span with applied style <span_style>    
    Then the calculated text size is <calculated_size>


    Examples:
    | cell_resolution | region_size | div_size | p_size | span_size | calculated_size |  
    | 32 15           | 100%        | 100%     | 100%   | 100%      | 1c              |  
    | 32 15           | 50%         | 200%     | 50%    | 200%      | 1c              |  
    | 32 15           | 1c          | 200%     | 100%   | 50%       | 1c              |  
    | 32 15           | 100%        | 2c       | 100%   | 50%       | 1c              |  
    | 10 10           | 100%        |          |        | 50%       | .5c             |  
    | 20 20           |             | 50%      |        | 400%      | 10%             |  
