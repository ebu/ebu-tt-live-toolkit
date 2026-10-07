
Feature: Configuration of websocket carriage
  # These examples hold a websocket carriage mechanism configuration for a producer-consumer pair of nodes

  Scenario Outline: Get parts of sequence
    Given an xml file "sequence_id_num.xml"
    And a configuration file "websocket_carriage_config.json"
    And a sequence with the following identifier and timeBase
      | sequence_identifier | time_base |
      | test                | media     |
    When a free port has been found
    And the producer listens on the port
    And the consumer connects to the port with <client_url_path>
    And the configuration file is loaded
    And producer sends document with <sequence_number_1>
    And producer sends document with <sequence_number_2>
    Then transmission should be successful

    Examples:
    | sequence_number_1 | sequence_number_2 | client_url_path         |
    | 1                 | 2                 | TestSequence1/subscribe |
