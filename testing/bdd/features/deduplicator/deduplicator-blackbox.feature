Feature: Deduplicator removes duplicated style and region elements

  Examples:
  | xml_file      |
  | test_file.xml |

  #Everything goes right
  Scenario: The deduplicator emits a document that has instances of duplicated <style> and <region> elements removed
     Given an <xml_file>
     And it has style element <style_element_1>
     And it has style element <style_element_2>
     And it has region element <region_element_1>
     And it has region element <region_element_2>
     And it has div style referencing <div_style>
     And it has a span style referencing <span_style>
     When the deduplicator node processes the document
     And the deduplicator node generates an output document
     Then the output document has style element id <new_style_label>
     And it has region element id <new_region_label>
     And it has div style referencing <new_region_label>
     And it has span style referencing <new_style_label>
     And it has sequence ID <sequenceID>
     And it has sequence number <sequenceNum>


      Examples:
        | style_element_1                                                                                                                                     | style_element_2                                                                                                                                     | new_style_label | region_element_1                                                                                                                                    | region_element_2                                                                                                                                    | new_region_label | div_region         | span_style          | sequenceID                                | sequenceNum               |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ59.defaultStyle1" | defaultStyle1   | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ59.bottomRegion" | bottomRegion1    | SEQ59.bottomRegion | SEQ58.defaultStyle1 | ebuttp:sequenceIdentifier="DeDuplicated1" | ebuttp:sequenceNumber="1" |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | defaultStyle1   | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | bottomRegion1    | SEQ58.bottomRegion | SEQ58.defaultStyle1 | ebuttp:sequenceIdentifier="DeDuplicated1" | ebuttp:sequenceNumber="1" |
        | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(255, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ58.defaultStyle1" | ebutts:linePadding="0.5c" tts:backgroundColor="rgb(0, 0, 0)" tts:color="rgb(0, 255, 255)" tts:fontFamily="sansSerif" xml:id="SEQ60.defaultStyle1"   | defaultStyle1   | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="14.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ58.bottomRegion" | tts:displayAlign="after" tts:extent="71.25% 24%" tts:origin="12.375% 60%" tts:overflow="visible" tts:writingMode="lrtb" xml:id="SEQ60.bottomRegion" | bottomRegion1    | SEQ60.bottomRegion | SEQ58.defaultStyle1 | ebuttp:sequenceIdentifier="DeDuplicated1" | ebuttp:sequenceNumber="1" |

#  Scenario: Upon receiving more than one file, the deduplicator reads each one sequentially and successfully removes instances of element duplication
#    Given the deduplicator receives more than one file

  #Everything goes wrong
  Scenario: The deduplicator does nothing if no files are present
    Given the deduplicator receives no files
    Then the process terminates
