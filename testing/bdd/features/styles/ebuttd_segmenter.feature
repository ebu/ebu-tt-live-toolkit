@styles @segmentation @document
Feature: Merge styles from different Part 3 documents into a single EBU-TT-D document


  # The overall assumption here is that we analyse the styles and create a new style definition for each unique combination of attributes and unique values
  # This means that we have to compute the style first, e.g. if style1 has tts:backgroundColor="black" and style2 has tts:backgroundColor="#000" then they will be merged (assuming other attributes are identical).
  # The naming rules for the merged styles are tested elsewhere.


  # Let's start simple: non-inherited attributes or ones with overwrite relationship to parent are merged if they have identical values.    
  Scenario: Merge identical non-multiplied styles
    Given two EBU-TT Live documents
    And document 1 has element with attribute <att_1> applied with value <val_1>
    And document 2 has element with attribute <att_2> applied with value <val_2>
    When we merge the documents and convert to an EBU-TT-D document
    Then the EBU-TT-D has a merged style with attribute <att_merged> with value <val_merged>  

    Examples:
    | att_1               | val_1  | att_2               | val_2   | att_merged          | val_merged |  
    | tts:backgroundColor | black  | tts:backgroundColor | #000000 | tts:backgroundColor | #000000    |  
    | tts:fontWeight      | normal | tts:fontWeight      | normal  | tts:fontWeight      | normal     |  


  # Same non-inherited or overwrite attributes but with different values, so no merging. Still not thinking about the parent.  
  Scenario: Do not merge different styles
    Given two EBU-TT Live documents
    And document 1 has element with attribute <att_1> applied with value <val_1>
    And document 2 has element with attribute <att_2> applied with value <val_2>
    When we merge the documents and convert to an EBU-TT-D document
    Then the EBU-TT-D has style 1 with attribute <att_merged_1> with value <val_merged_1>  
    And the EBU-TT-D has style 2 with attribute <att_merged_2> with value <val_merged_2>  

    Examples:
    | att_1               | val_1  | att_2               | val_2   | att_merged_1        | val_merged_1 | att_merged_2        | val_merged_2 |  
    | tts:backgroundColor | white  | tts:backgroundColor | #000000 | tts:backgroundColor | white        | tts:backgroundColor | #000000      |  
    | tts:fontWeight      | normal | tts:fontWeight      | bold    | tts:fontWeight      | normal       | tts:fontWeight      | bold         |  


  # NOT SURE THIS IS CORRECT - CAN WE HAVE <num_merged_styles>?
  # Make sure that unique styles are created for each unique combination of attribute and value. Parents not involved. 
  Scenario: Unique styles are not merged
    Given two EBU-TT Live documents
    And document 1 has element 1 with attribute <style_1_att_1> applied with value <style_1_val_1>
    And document 1 has element 1 with attribute <style_1_att_2> applied with value <style_1_val_2>
    And document 2 has element 2 with attribute <style_2_att_1> applied with value <style_2_val_1>
    And document 2 has element 2 with attribute <style_2_att_2> applied with value <style_2_val_2>
    When we merge the documents and convert to an EBU-TT-D document
    Then the EBU-TT-D has number of style definitions <num_merged_styles>  # can we do this? If not, how to express the number of styles created?  

    Examples:
    | style_1_att_1       | style_1_val_1 | style_1_att_2 | style_1_val_2 | style_2_att_1       | style_2_val_1 | style_2_att_2 | style_2_val_2 | num_merged_styles |  
    | tts:backgroundColor | black         | fontWeight    | normal        | tts:backgroundColor | black         | fontWeight    | normal        | 1                 |  
    | tts:backgroundColor | black         | fontWeight    | normal        | tts:backgroundColor | black         | fontWeight    | bold          | 2                 |  
    | tts:backgroundColor | #000          | fontWeight    | normal        | tts:backgroundColor | black         | fontWeight    | normal        | 1                 |  
    | tts:backgroundColor | black         | fontWeight    | normal        | tts:backgroundColor | white         | fontWeight    | bold          | 2                 |  


  






#   Examples:
#   | cell_resolution_1 | parent_1_fontSize | child_1_fontSize | cell_resolution_2 | parent_2_fontSize | child_2_fontSize | merged_cell_resolution | merged_fontSize |  
#   | 32 15             | 1c                |                  | 32 15             |                   | 1c               | 32 15                  | 100%            |  
#   | 32 15             | .5c               | 1c               | 32 15             | 1c                |                  | 32 15                  | 100%            |  
#   | 32 15             | 1c                |                  | 64 30             | 2c                |                  | 32 15                  | 100%            |  
#   | 32 15             | 1c 2c             | 1c               | 32 15             | 2c 1c             | 1c               | 32 15                  | 100%            |  
#   | 32 15             | 1c 2c             | 1c               | 32 15             | 2c 1c             | 1c               | 32 15                  | 100%            |  
#   | 64 30             | 1c                | 2c               | 32 15             | 1c                |                  | 64 30                  | 100%            |

  #TODO: create separate styles when the computed styles are different
