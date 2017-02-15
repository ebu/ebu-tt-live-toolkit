
Feature: Configuration of websocket carriage
  # These examples hold a websocket carriage mechanism configuration for a producer-consumer pair of nodes

  Examples:
  | config_file                    | xml_file            | sequence_identifier | time_base |
  | websocket_carriage_config.json | sequence_if_num.xml | test                | media     |

  Scenario: Get parts of sequence
    Given an xml file <xml_file>
    And a settings file <settings_file>
    And a sequence <sequence_identifier> with timeBase <time_base>
    When a free port has been found
    And the producer listens on the port
    And the consumer connects to the port with <client_url_path>
    And producer sends document with <sequence_number_1>
    And producer sends document with <sequence_number_2>
    Then transmission should be successful

    Examples:
    | sequence_number_1 | sequence_number_2 | client_url_path |
    |                   |                   |                 |
