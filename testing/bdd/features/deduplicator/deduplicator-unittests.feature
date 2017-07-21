Feature: Deduplicator removes duplicated elements

  Background:
    Given an xml file <xml_file>
      | xml_file      |
      | test_file.xml |

  Scenario: a successfully deduplicated document
    Given an xml document
    When it has style1 with attributes <style_1_attrs>
    And it has style2 with attributes <style_2_attrs>
    And it has region1 with attributes <region_1_attrs>
    And it has region2 with attribtues <region_2_attrs>
    And it has div1 with attributes <div_1_attrs>
    And it has span1 with attributes <span_1_attrs>
    And it has div2 with attributes <div_2_attrs>
    And it has span2 with attributes <span_2_attrs>
    When it is deduplicated
    Then the output document has <out_styles> styles
    And the output document has <out_regions> regions
    And the output document has <out_div> divs
    And the output document has <out_span> spans
    And the document is valid

      Examples:
        | style_1_attrs                                                                                                                                       | style_2_attrs                                                                                                                                       | region_1_attrs                                                                                                                                      | region_2_attrs                                                                                                             | div_1_attrs                 | span_1_attrs                | div_2_attrs                 | span_2_attrs                | out_styles                                                                                                                                          | out_regions                                                                                        | out_div                     | out_span |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ59.defaultStyle1" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | region="SEQ58.bottomRegion" | style="SEQ58.defaultStyle1" | region="SEQ59.bottomRegion" | style="SEQ59.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | region="SEQ58.bottomRegion" | style="SEQ58.defaultStyle1" |
        
#  Scenario: assign new label to an element
#    Then the <xml_id> is replaced by <new_label>
#
#      Examples:
#        | xml_id              | new_label     |
#        | SEQ58.defaultStyle1 | defaultStyle1 |
#        | SEQ58.bottomRegion  | bottomRegion1 |

#  Scenario: assign same label to duplicate elements
#    When it has style attributes <style_1>
#    And it has style attributes <style_2>
#    And <style_1> and <style_2> are the same
#    Then name of <id_1>
#    And name of <id_2> are replaced with the same <new_label>

#      Examples:
#        | style_1                                                                                                                 | style_2                                                                                                                 | id_1                | id_2                | new_label           |
#        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif"  | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif"  | SEQ58.defaultStyle1 | SEQ59.defaultStyle1 | SEQ58.defaultStyle1 |
#        | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" | SEQ58.bottomRegion  | SEQ59.bottomRegion  | SEQ58.bottomRegion1 |

#  Scenario: assign different labels to different elements
#    When it has style attributes <style_1>
#    And it has style attributes <style_2>
#    And <style_1> and <style_2> are not the same
#    Then name of <id_1> is replaced with <new_label_1>
#    And name of <id_2> is replaced with <new_label_2>

#      Examples:
#        | style_1                                                                                                                 | style_2                                                                                                                 | id_1                | new_label_1         | id_2                | new_label_2         |
#        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(0, 255, 255)" tts:fontFamily="sansSerif"    | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif"  | SEQ58.defaultStyle1 | SEQ58.defaultStyle1 | SEQ59.defaultStyle1 | SEQ59.defaultStyle2 |
#        | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" | tts:displayAlign="after" tts:extent="50.75% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" | SEQ58.bottomRegion  | SEQ58.bottomRegion1 | SEQ59.bottomRegion  | SEQ59.bottomRegion2 |

#  Scenario: assign correct label to element references
#    When it has element name <element_name>
#    And it has old id <old_id>
#    Then replace with <new_label> if they are the same

#      Examples:
#        | element_name        | old_id              | new_label           |
#        | SEQ58.defaultStyle1 | SEQ58.defaultStyle1 | SEQ58.defaultStyle1 |
#        | SEQ58.bottomRegion  | SEQ58.bottomRegion  | SEQ58.bottomRegion1 |

#  Scenario: remove duplication from in-line style references
#    When it has a reference <old_style_reference>
#    Then replace with <new_style_reference>

#      Examples:
#        | old_style_reference                                          | new_syle_reference                      |
#        | SEQ58.defaultStyle1 SEQ59.defualt.styled SEQ60.defaultStyle1 | SEQ58.defaultStyle1 SEQ60.defaultStyle1 |
