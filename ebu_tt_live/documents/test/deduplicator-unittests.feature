Feature: Deduplicator removes duplicated elements

Examples:
| xml_file             |
| resequenced_file.xml |

Scenario: assign new label to an element
  Given an xml file <xml_file>
  And an element with <xml_id>
  Then the id is replaced by <new_label>

Examples:
| xml_id              | new_label     |
| SEQ58.defaultStyle1 | defaultStyle1 |
| SEQ58.bottomRegion  | bottomRegion1 |

Scenario: assign same label to duplicate elements
  Given an xml file <xml_file>
  When contents of <style_1>
  And contents of <style_2> are the same
  Then name of <id_1>
  And name of <id_2> are replaced with the same <new_label>

Examples:
| style_1                                                                                                                     | style_2                                                                                                                     | id_1                | id_2                | new_label     |
| ebutts:linePadding="0.5c", tts:backgroundColor="rgb(0, 0, 0)", tts:color="rgb(255, 255, 255)", tts:fontFamily="sansSerif"   | ebutts:linePadding="0.5c", tts:backgroundColor="rgb(0, 0, 0)", tts:color="rgb(255, 255, 255)", tts:fontFamily="sansSerif"   | SEQ58.defaultStyle1 | SEQ59.defaultStyle1 | defaultStyle1 |
| tts:displayAlign="after", tts:extent="71.25% 24%", tts:origin="14.375% 60%", tts:overflow="visible", tts:writingMode="lrtb" | tts:displayAlign="after", tts:extent="71.25% 24%", tts:origin="14.375% 60%", tts:overflow="visible", tts:writingMode="lrtb" | SEQ58.bottomRegion  | SEQ59.bottomRegion  | bottomRegion1 |

Scenario: assign different labels to different elements
  Given an xml file <xml_file>
  When contents of <style_1>
  And contents of <style_2> are not the same
  Then name of <id_1> is replaced with <new_label_1>
  And name of <id_2> is replaced with <new_label_2>

Examples:
| style_1                                                                                                                     | style_2                                                                                                                     | id_1                | new_label_1   | id_2                | new_label_2   |
| ebutts:linePadding="0.5c", tts:backgroundColor="rgb(0, 0, 0)", tts:color="rgb(0, 255, 255)", tts:fontFamily="sansSerif"     | ebutts:linePadding="0.5c", tts:backgroundColor="rgb(0, 0, 0)", tts:color="rgb(255, 255, 255)", tts:fontFamily="sansSerif"   | SEQ58.defaultStyle1 | defaultStyle1 | SEQ59.defaultStyle1 | defaultStyle2 |
| tts:displayAlign="after", tts:extent="71.25% 24%", tts:origin="14.375% 60%", tts:overflow="visible", tts:writingMode="lrtb" | tts:displayAlign="after", tts:extent="50.75% 24%", tts:origin="14.375% 60%", tts:overflow="visible", tts:writingMode="lrtb" | SEQ58.bottomRegion  | bottomRegion1 | SEQ59.bottomRegion  | bottomRegion2 |

Scenario: assign correct label to element references
  Given an xml file <xml_file>
  When <element_name> matches <stored_name>
  Then replace with <new_label>

Examples:
| element_name        | stored_name         | new_label     |
| SEQ58.defaultStyle1 | SEQ58.defaultStyle1 | defaultStyle1 |
| SEQ58.bottomRegion  | SEQ58.bottomRegion  | bottomRegion1 |
