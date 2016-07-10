# Conformance Requirements list for EBU-TT Part 3 Tech3370

The conformance requirements for EBU-TT Part 3 derive from the specification itself, EBU-TT Part 1, TTML1SE and their referenced specifications - SMIL, XSL-FO etc. The following normative statements are present in Tech3370:

## SHALL requirements

|ID|Section|Statement|Test|
|---|---|---|---|---|
| | **Tech3370**| | |
| R1|2.2|When presenting a sequence of documents, at each moment in time exactly zero or one document shall be active.| |
| R2|2.2 |If no document is active, or if a document with no content is active, no content shall be displayed. | |
| R3|2.2 |Sequences shall be considered distinct if they have had processing applied, even if the result of that processing is no change other than a known difference in state, for example if the processing has checked the spelling of the text content.| |
| R4|2.2 |Every distinct sequence shall have a unique sequence identifier.| |
| R5|2.2 |A document shall be associated with exactly one sequence.| |
| R6|2.2 |the sequence identifier shall be present within every document| |
| R7|2.2 |Documents with the same sequence identifier shall contain a sequence number.| |
| R8|2.2 |Every distinct document with the same sequence identifier shall have a different sequence number.| |
| R9|2.2 |Sequence numbers shall increase with the passage of time for each new document that is made available.| |
|R10|2.2 |Every document in a sequence shall be valid and self-contained.| |
|R11|2.2 |Every document in a sequence shall have an identical timing model as defined by using the same values for the `ttp:timeBase` and `ttp:clockMode` attributes. (Note issue to add `frameRate`, `frameRateMultiplier` and `dropMode` to this attribute set)| |
|R12|2.2 |A passive node shall NOT modify input sequences and shall only emit sequences that are identical (including the sequence numbers) to the input sequence(s)| |
|R13|2.2 |At any moment in the presentation of a sequence by a node exactly zero or one document shall be temporally active.| |
|R14|2.3.1|At any single moment in time during the presentation of a sequence either zero documents or one document shall be active.| |
|R15|2.3.1 |The period during which a document is active begins at the document resolved begin time and ends at the document resolved end time.| |
|R16|2.3.1.1|The document resolved begin time shall be the later of (a) the document availability time, (b) the earliest computed begin time in the document and (c) any externally specified document activation begin time, such as the beginning of sequence presentation.| |
|R17|2.3.1.2|The document resolved end time shall be the earlier of (a) the earliest document resolved begin time of all available documents in the sequence with a greater sequence number, (b) the document resolved begin time plus the value of the `dur` attribute, if present, (c) the latest computed end time in the document and (d) any externally specified document deactivation time, such as the end of sequence presentation.| |
|R18|2.3.1.3|When no document is active a presentation processor shall NOT render any content.| |
|R19|2.3.4|A Delay node is a processing node. Therefore the output sequence shall have a different sequence identifier from the input sequence.| |
|R20|2.3.4|A Delay node may emit implicitly timed documents within a sequence. In this case the Delay node shall delay emission of the stream by a period equivalent to the adjustment value.| |
|R21|2.3.4|A Delay node shall NOT emit an output sequence with reordered subtitles.| |
|R22|2.3.4|A Delay node shall NOT update the value of `ebuttm:authoringDelay`.| |
|R23|2.4|The Handover Manager node shall use a 'who claimed control most recently' algorithm for selecting the sequence, based on a control token parameter within each document.| |
|R24|2.4.1|All documents within a sequence that contain the element `ebuttp:authorsGroupIdentifier` shall have the same `ebuttp:authorsGroupIdentifier`.| |
|R25|2.4.1|when a document is received with a higher value `ebuttp:authorsGroupControlToken` than that most recently received in the currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it shall emit a document in its output sequence corresponding to the received document with the new control token without delay.| |
|R26|2.5|it is an error to apply more than one `facet` with the same term identifier to the same content element, where the term identifier is the combination of the term name and the link attribute's value.| |
|R27|2.5.1|If all the content in a document has a `facet` then the summary shall be `"all\_has"`.| |
|R28|2.5.1|If all the content in a document has\_not a `facet` then the summary shall be `"all\_has_not"`.| |
|R29|2.5.1|If there is a mix of has and has\_not and unknown or if some of the content does not have the `facet` then the summary shall be `"mixed"`.| |
|R30|2.5.1|If none of the document's content has the `facet` or all of the document's content has the `facet` described as unknown then the summary shall be `"unspecified"`.| |
|R31|2.6|If present, a `trace` element shall describe in text the action that generated the document, in the action attribute, and an identifier that performed that action, in the `generatedBy` attribute.| |
|R32|3.2.2.1|`ttp:timeBase` Cardinality 1..1| |
|R33|3.2.2.1|The `ttp:timeBase` element is as defined in [EBUTT1] with the addition that all time expressions of `dur` attributes shall denote a relative coordinate on the same timeline as the `begin` and `end` attributes.| |
|R34|3.2.2.1|`ebuttp:sequenceIdentifier` Cardinality 1..1| |
|R35|3.2.2.1|The sequence to which every document belongs shall be identified using the `ebuttp:sequenceIdentifier` attribute.| |
|R36|3.2.2.1|`ebutt:sequenceNumber` Cardinality 1..1| |
|R37|3.2.2.1|Every document with the same `ebuttp:sequenceIdentifier` shall be uniquely numbered using the `ebuttp:sequenceNumber` attribute.| |
|R38|3.2.2.2|The following additional metadata elements are defined by this specification. If used these elements shall be the first children of the `ebuttm:documentMetadata` element in the order documented below, after any metadata elements defined by EBU-TT Part 1 Tech 3350.| |
|R39|3.2.2.2|Order of metadata elements (if present) in `ebuttm:documentMetadata` is: `ebuttm:originalSourceServiceIdentifier`, `ebuttm:intendedDestinationServiceIdentifier`, `ebuttm:documentFacet`, `ebuttm:trace`. | |
|R40|3.2.2.2|`ebuttm:documentFacet` : Each distinctly identified `facet` that is summarised shall have a separate `documentFacet` element.| |
|R41|3.2.2.2|Documents shall NOT contain more than one `documentFacet` element referring to the same term, where the term is identified by the combination of the element contents and the value of the link attribute.| |
|R42|3.2.2.2.1| `ebuttm:trace` `action` attribute Cardinality 1..1 | |
|R43|3.2.2.2.1| `ebuttm:trace` `generatedBy` attribute Cardinality 1..1 | |
|R44|3.2.2.3| A document that contains a `tt:body` element with no content shall be treated as being active as defined by the semantics described in § 2.3.1, and shall cause no content to be presented while it is active.| |
|R45|3.2.2.3|`body` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | |
|R46|3.2.2.3|`body` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R47|3.2.2.3|`body` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R48|3.2.2.3|`body` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | |
|R49|3.2.2.3|`body` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R50|3.2.2.3|`body` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R51|3.2.2.3|`body` `dur` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. (NB this will be permitted when `markerMode="continuous"`, a change yet to be implemented in the spec)| |
|R52|3.2.2.3|`body` `dur` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R53|3.2.2.3|`body` `dur` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R54|3.2.2.4|`div` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | |
|R55|3.2.2.4|`div` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R56|3.2.2.4|`div` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R57|3.2.2.4|`div` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | |
|R58|3.2.2.4|`div` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R59|3.2.2.4|`div` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R60|3.2.2.5|`p` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | |
|R61|3.2.2.5|`p` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R62|3.2.2.5|`p` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R63|3.2.2.5|`p` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | |
|R64|3.2.2.5|`p` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | |
|R65|3.2.2.5|`p` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | |
|R66|3.2.2.6.1|Each distinctly identified facet shall have a separate `facet` element, where facets are identified by combination of the text content and the link attribute.| |
|R67|3.2.2.6.1|Elements shall NOT contain more than one `facet` element referring to the same term.| |
|R68|3.3.1| `ebuttdt:delayTimingType` The content shall be constrained to a signed (positive or negative) number with an optional decimal fraction, followed by a time metric being one of: "h" (hours), "m" (minutes), "s" (seconds), "ms" (milliseconds).| |
