Feature: Deduplicator removes duplicated style and region elements

  Examples:
  | xml_file      |
  | test_file.xml |

  #Everything goes right
  Scenario: The deduplicator successfully removes instances of element duplication from a file
    Given the deduplicator receives one file
    Then it replaces instances of duplicated style elements
    And instances of duplicated region elements with new labels
    And outputs a new file with a new sequenceIdentifier and sequenceNumber

      Examples:
        | style_element                                                                                                                                       | style_compared_against                                                                                                                              | new_style_label | region_element                                                                                                                                      | region_compared_against                                                                                                                             | new_region_label | sequenceID                                | sequenceNum               |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ59.defaultStyle1" | defaultStyle1   | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ59.bottomRegion" | bottomRegion1    | ebuttp:sequenceIdentifier="DeDuplicated1" | ebuttp:sequenceNumber="1" |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | defaultStyle1   | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | bottomRegion1    | ebuttp:sequenceIdentifier="DeDuplicated1" | ebuttp:sequenceNumber="1" |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(0, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ60.defaultStyle1"   | defaultStyle1   | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="12.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ60.bottomRegion" | bottomRegion1    | ebuttp:sequenceIdentifier="DeDuplicated1" | ebuttp:sequenceNumber="1" |

#  Scenario: Upon receiving more than one file, the deduplicator reads each one sequentially and successfully removes instances of element duplication
#    Given the deduplicator receives more than one file

  #Everything goes wrong
  Scenario: The deduplicator does nothing if no files are present
    Given the deduplicator receives no files
    Then the process terminates
