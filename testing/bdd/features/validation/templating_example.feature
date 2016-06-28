Feature: Bindings
    Bindings map xsd and xml

    Scenario: From xml to binding (wrongs)
        Given a xml file <xml_file>
        And it has sequence identifier <seqID>
        And it has sequence number <seqN>
        Then the document is invalid

        Examples:
        | xml_file | seqID    | seqN |
        | base.xml |          | 5    |
        | base.xml | testSeq1 | a    |
