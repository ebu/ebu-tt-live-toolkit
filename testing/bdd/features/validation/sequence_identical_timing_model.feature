@validation @sequence
Feature: Every document in a sequence shall have an identical timing model as defined by using the same values for the 
  ttp:timeBase, ttp:clockMode, frameRate, frameRateMultiplier and dropMode attributes.

  Examples:
  | xml_file                             |
  | sequence_identical_timing_model.xml |

  # SPEC-CONFORMANCE: R11
  # GPS clock and SMPTE clock are not implemented yet so all the corresponding tests are skipped.
  Scenario: Not compatible document
    Given a test sequence
    And an xml file <xml_file>
    When it has sequenceNumber 1
    And it has timeBase <time_base1>
    And it has clockMode <clock_mode1>
    And it has frameRate <frame_rate1>
    And it has frameRateMultiplier <frame_rate_multiplier1>
    And it has dropMode <drop_mode1>
    And it has markerMode <marker_mode1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 2
    And it has timeBase <time_base2>
    And it has clockMode <clock_mode2>
    And it has frameRate <frame_rate2>
    And it has frameRateMultiplier <frame_rate_multiplier2>
    And it has dropMode <drop_mode2>
    And it has markerMode <marker_mode2>
    Then adding doc2 to the sequence results in an error

    Examples:
    | time_base1 | clock_mode1 | frame_rate1 | frame_rate_multiplier1 | drop_mode1 | marker_mode1 | time_base2 | clock_mode2 | frame_rate2 | frame_rate_multiplier2 | drop_mode2 | marker_mode2 |
    | clock      | local       |             |                        |            |              | clock      | utc         |             |                        |            |              |
    | clock      | utc         |             |                        |            |              | clock      | gps         |             |                        |            |              |
    | media      |             |             |                        |            |              | clock      | local       |             |                        |            |              |
    @skip
    | clock      | gps         |             |                        |            |              | clock      | local       |             |                        |            |              |
    | clock      | local       |             |                        |            |              | smpte      |             | 25          | 1 1                    | nonDrop    | continuous   |
    | media      |             |             |                        |            |              | smpte      |             | 25          | 1 1                    | nonDrop    | continuous   |
    | smpte      | smpte       | 20          | 1 1                    | nonDrop    | continuous   | smpte      |             | 25          | 1 1                    | nonDrop    | continuous   |
    | smpte      | smpte       | 30          | 1000 1001              | dropPal    | continuous   | smpte      |             | 30          | 1 1                    | nonDrop    | continuous   |
    | smpte      | smpte       | 30          | 1000 1001              | dropPal    | continuous   | smpte      |             | 30          | 1000 1001              | dropNTSC   | continuous   |


  # SPEC-CONFORMANCE: R11
  Scenario: Compatible document
    Given a test sequence
    And an xml file <xml_file>
    When it has sequenceNumber 1
    And it has timeBase <time_base1>
    And it has clockMode <clock_mode1>
    And it has frameRate <frame_rate1>
    And it has frameRateMultiplier <frame_rate_multiplier1>
    And it has dropMode <drop_mode1>
    And it has markerMode <marker_mode1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 2
    And it has timeBase <time_base2>
    And it has clockMode <clock_mode2>
    And it has frameRate <frame_rate2>
    And it has frameRateMultiplier <frame_rate_multiplier2>
    And it has dropMode <drop_mode2>
    And it has markerMode <marker_mode2>
    Then adding doc2 to the sequence does not raise any error

    Examples:
    | time_base1 | clock_mode1 | frame_rate1 | frame_rate_multiplier1 | drop_mode1 | marker_mode1 | time_base2 | clock_mode2 | frame_rate2 | frame_rate_multiplier2 | drop_mode2 | marker_mode2 |
    | clock      | local       |             |                        |            |              | clock      | local       |             |                        |            |              |
    | clock      | utc         |             |                        |            |              | clock      | utc         |             |                        |            |              |
    @skip
    | clock      | gps         |             |                        |            |              | clock      | gps         |             |                        |            |              |
    | media      |             |             |                        |            |              | media      |             |             |                        |            |              |
    | smpte      |             | 25          | 1 1                    | nonDrop    | continuous   | smpte      |             | 25          | 1 1                    | nonDrop    | continuous   |
