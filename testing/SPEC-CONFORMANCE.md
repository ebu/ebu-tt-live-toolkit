# Conformance Requirements list for EBU-TT Part 3 Tech 3370

The conformance requirements for EBU-TT Part 3 derive from the specification itself, EBU-TT Part 1, TTML1SE and their referenced specifications - SMIL, XSL-FO etc. The following normative statements are present in Tech 3370:

## SHALL requirements

|ID|Section|Statement|Feature file path and Scenario name|
|---|---|---|---|---|
| | **Tech3370**| | |
| R1|2.2|When presenting a sequence of documents, at each moment in time exactly zero or one document shall be active.| |
| R2|2.2 |If no document is active, or if a document with no content is active, no content shall be displayed. | |
| R3|2.2 |Sequences shall be considered distinct if they have had processing applied, even if the result of that processing is no change other than a known difference in state, for example if the processing has checked the spelling of the text content.| |
| R4|2.2 |Every distinct sequence shall have a unique sequence identifier.| |
| R5|2.2 |A document shall be associated with exactly one sequence.| |
| R6|2.2 |the sequence identifier shall be present within every document|`bdd/features/validation/sequence\_id\_num.feature` `(In)valid Sequence head attributes`|
| R7|2.2 |Documents with the same sequence identifier shall contain a sequence number.|`bdd/features/validation/sequence\_id\_num.feature` `(In)valid Sequence head attributes`|
| R8|2.2 |Every distinct document with the same sequence identifier shall have a different sequence number.| |
| R9|2.2 |Sequence numbers shall increase with the passage of time for each new document that is made available.|`../ebu\_tt\_live/documents/test/test\_ebutt3sequence.py` `test\_increasing\_sequence\_number`|
|R10|2.2 |Every document in a sequence shall be valid and self-contained.| |
|R11|2.2 |Every document in a sequence shall have an identical timing model as defined by using the same values for the `ttp:timeBase` and `ttp:clockMode` attributes. (Note issue to add `frameRate`, `frameRateMultiplier` and `dropMode` to this attribute set)|`bdd/features/validation/sequence\_identical\_timing\_model.feature` `(Not) compatible document`|
|R12|2.2 |A passive node shall NOT modify input sequences and shall only emit sequences that are identical (including the sequence numbers) to the input sequence(s)| |
|R13|2.2 |At any moment in the presentation of a sequence by a node exactly zero or one document shall be temporally active.| |
|R14|2.3.1|At any single moment in time during the presentation of a sequence either zero documents or one document shall be active.| |
|R15|2.3.1 |The period during which a document is active begins at the document resolved begin time and ends at the document resolved end time.| |
|R16|2.3.1.1|The document resolved begin time shall be the later of (a) the document availability time, (b) the earliest computed begin time in the document and (c) any externally specified document activation begin time, such as the beginning of sequence presentation.|`bdd/features/timing/resolved\_times.feature`|
|R17|2.3.1.2|The document resolved end time shall be the earlier of (a) the earliest document resolved begin time of all available documents in the sequence with a greater sequence number, (b) the document resolved begin time plus the value of the `dur` attribute, if present, (c) the latest computed end time in the document and (d) any externally specified document deactivation time, such as the end of sequence presentation.|`bdd/features/timing/resolved\_times.feature`|
|R18|2.3.1.3|When no document is active a presentation processor shall NOT render any content.| |
|R19|2.3.4|A Delay node is a processing node. Therefore the output sequence shall have a different sequence identifier from the input sequence.| |
|R20|2.3.4|A Delay node may emit implicitly timed documents within a sequence. In this case the Delay node shall delay emission of the stream by a period equivalent to the adjustment value.| |
|R21|2.3.4|A Delay node shall NOT emit an output sequence with reordered subtitles.| |
|R22|2.3.4|A Delay node shall NOT update the value of `ebuttm:authoringDelay`.| |
|R23|2.4|The Handover Manager node shall use a 'who claimed control most recently' algorithm for selecting the sequence, based on a control token parameter within each document.| |
|R24|2.4.1|All documents within a sequence that contain the element `ebuttp:authorsGroupIdentifier` shall have the same `ebuttp:authorsGroupIdentifier`.| |
|R25|2.4.1|when a document is received with a higher value `ebuttp:authorsGroupControlToken` than that most recently received in the currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it shall emit a document in its output sequence corresponding to the received document with the new control token without delay.| |
|R26|2.5|it is an error to apply more than one `facet` with the same term identifier to the same content element, where the term identifier is the combination of the term name and the link attribute's value.|`bdd/features/validation/facet.feature` `(In)valid term identifier`|
|R27|2.5.1|If all the content in a document has a `facet` then the summary shall be `"all\_has"`.| `bdd/features/validation/facet.feature` `(In)valid term identifier`|
|R28|2.5.1|If all the content in a document has\_not a `facet` then the summary shall be `"all\_has_not"`.|`bdd/features/validation/facet.feature` `(In)valid facet summary` |
|R29|2.5.1|If there is a mix of has and has\_not and unknown or if some of the content does not have the `facet` then the summary shall be `"mixed"`.|`bdd/features/validation/facet.feature` `(In)valid facet summary` |
|R30|2.5.1|If none of the document's content has the `facet` or all of the document's content has the `facet` described as unknown then the summary shall be `"unspecified"`.| `bdd/features/validation/facet.feature` `(In)valid facet summary`|
|R31|2.6|If present, a `trace` element shall describe in text the action that generated the document, in the action attribute, and an identifier that performed that action, in the `generatedBy` attribute.|`bdd/features/validation/trace.feature` `(In)valid trace attributes`|
|R32|3.2.2.1|`ttp:timeBase` Cardinality 1..1|`bdd/features/validation/timeBase_attribute_mandatory.feature` `(In)valid ttp:timeBase`|
|R33|3.2.2.1|The `ttp:timeBase` element is as defined in [EBUTT1] with the addition that all time expressions of `dur` attributes shall denote a relative coordinate on the same timeline as the `begin` and `end` attributes.| |
|R34|3.2.2.1|`ebuttp:sequenceIdentifier` Cardinality 1..1|`bdd/features/validation/sequence\_id\_num.feature` `(In)valid Sequence head attributes`|
|R35|3.2.2.1|The sequence to which every document belongs shall be identified using the `ebuttp:sequenceIdentifier` attribute.|`bdd/features/validation/sequence\_id\_num.feature` `(In)valid Sequence head attributes`|
|R36|3.2.2.1|`ebutt:sequenceNumber` Cardinality 1..1|`bdd/features/validation/sequence\_id\_num.feature` `(In)valid Sequence head attributes`|
|R37|3.2.2.1|Every document with the same `ebuttp:sequenceIdentifier` shall be uniquely numbered using the `ebuttp:sequenceNumber` attribute.| |
|R38|3.2.2.2|The following additional metadata elements are defined by this specification. If used these elements shall be the first children of the `ebuttm:documentMetadata` element in the order documented below, after any metadata elements defined by EBU-TT Part 1 Tech 3350.|`bdd/features/validation/documentMetadata_elements_order.feature` `(In)valid documentMetadata elements order`|
|R39|3.2.2.2|Order of metadata elements (if present) in `ebuttm:documentMetadata` is: `ebuttm:originalSourceServiceIdentifier`, `ebuttm:intendedDestinationServiceIdentifier`, `ebuttm:documentFacet`, `ebuttm:trace`. |`bdd/features/validation/documentMetadata_elements_order.feature` `(In)valid documentMetadata elements order`|
|R40|3.2.2.2|`ebuttm:documentFacet` : Each distinctly identified `facet` that is summarised shall have a separate `documentFacet` element.| |
|R41|3.2.2.2|Documents shall NOT contain more than one `documentFacet` element referring to the same term, where the term is identified by the combination of the element contents and the value of the link attribute.| |
|R42|3.2.2.2.1| `ebuttm:trace` `action` attribute Cardinality 1..1 |`bdd/features/validation/trace.feature` `(In)valid trace attributes`|
|R43|3.2.2.2.1| `ebuttm:trace` `generatedBy` attribute Cardinality 1..1 |`bdd/features/validation/trace.feature` `(In)valid trace attributes`|
|R44|3.2.2.3| A document that contains a `tt:body` element with no content shall be treated as being active as defined by the semantics described in § 2.3.1, and shall cause no content to be presented while it is active.| |
|R45|3.2.2.3|`body` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in body` |
|R46|3.2.2.3|`body` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase`|
|R47|3.2.2.3|`body` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase`|
|R48|3.2.2.3|`body` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in body` |
|R49|3.2.2.3|`body` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase`|
|R50|3.2.2.3|`body` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase`|
|R51|3.2.2.3|`body` `dur` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. (NB this will be permitted when `markerMode="continuous"`, a change yet to be implemented in the spec)|`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in body` |
|R52|3.2.2.3|`body` `dur` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase`|
|R53|3.2.2.3|`body` `dur` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase`|
|R54|3.2.2.4|`div` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature (In)valid times according to timeBase in div`|
|R55|3.2.2.4|`div` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in div`|
|R56|3.2.2.4|`div` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in div`|
|R57|3.2.2.4|`div` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature (In)valid times according to timeBase in div` |
|R58|3.2.2.4|`div` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in div` |
|R59|3.2.2.4|`div` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in div`|
|R60|3.2.2.5|`p` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in p`|
|R61|3.2.2.5|`p` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in p`|
|R62|3.2.2.5|`p` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in p`|
|R63|3.2.2.5|`p` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in p`|
|R64|3.2.2.5|`p` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in p`|
|R65|3.2.2.5|`p` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in p`|
|R66|3.2.2.6.1|Each distinctly identified facet shall have a separate `facet` element, where facets are identified by combination of the text content and the link attribute.|`bdd/features/validation/facet.feature` `(In)valid term identifier`|
|R67|3.2.2.6.1|Elements shall NOT contain more than one `facet` element referring to the same term.|`bdd/features/validation/facet.feature` `(In)valid term identifier`|
|R68|3.3.1| `ebuttdt:delayTimingType` The content shall be constrained to a signed (positive or negative) number with an optional decimal fraction, followed by a time metric being one of: "h" (hours), "m" (minutes), "s" (seconds), "ms" (milliseconds).|`bdd/features/delayTimingType.feature` `(In)valid delayTimingType format`|
| | **Tech3350 v1.1**| | |
|R69|3|If `ttp:timeBase="smpte"` then the time expression of `begin` and `end`  SHALL have the format hh:mm:ss:ff|`bdd/features/validation/timeBase\_timeformat\_constraints.feature`|
|R70|3|If `ttp:timeBase="media"` then the time expression of `begin` and `end` attributes SHALL have one of the following formats: (1) hh:mm:ss followed by an optional decimal fraction (full-clock value). The number of hours SHALL NOT be restricted. (2) Non-negative number followed by an optional decimal fraction followed by one of the symbols h, m, s, ms (time-count value)|`bdd/features/validation/timeBase\_timeformat\_constraints.feature`|
|R71|3|If `timebase="smpte"` then the attributes `ttp:markerMode`, `ttp:frameRate` and `ttp:dropMode` SHALL be specified on `tt:tt`|`bdd/features/validation/smpte\_constraints.feature` `(In)valid SMPTE head attributes`|
|R72|3|If `timebase="smpte"` then `ttp:markerMode` SHALL be specified and shall have the value `continuous` or the value `discontinuous`.|`bdd/features/validation/smpte\_constraints.feature` `(In)valid SMPTE head attributes`|
|R73a|3|If `timebase="smpte"` and the calculation of the frame rate from  `ttp:frameRate` and `ttp:frameRateMultiplier` results in an integer, then the value of `ttp:dropMode` SHALL be `nonDrop`.|`bdd/features/validation/smpte\_constraints.feature` `(In)valid SMPTE head attributes`|   
|R73b|3|If `ttp:timeBase="clock"` then `ttp:clockMode` SHALL be specified|`bdd/features/validation/timeBase_clock_clockMode_mandatory.feature` `(In)valid clock ttp:clockMode`|
|R74|3|`ttp:cellResolution` SHALL have the default value `32 15`.||
|R75|3|If the `cell` unit is used, `ttp:cellResolution` SHALL be specified. ||
|R76|3|If the `pixel` unit is used, `tts:extent` SHALL be specified on `tt:tt`||
|R77|3|`xml:lang` SHALL be specified on `tt:tt`|`bdd/features/validation/xml\_lang\_attribute.feature` `(In)valid xml:lang attribute`|
|R78|3.1.1.1.8|If `ebuttm:documentTargetActiveFormatDescriptor` is specified then `ebuttm:documentTargetAspectRatio` SHALL be specified with one of the values `4:3` or `16:9`||
|R79|3.1.1.1.8|If specified, `ebuttm:documentTargetActiveFormatDescriptor` SHALL have one of the AFD codes specified in SMPTE ST 2016-1:2009||
|R80|3.1.1.1.9|If specified, `ebuttm:documentIntendedTargetBarData` SHALL be specified in accordance with SMPTE ST2016-1:2009 Table 3||
|R81|3.1.1.1.9|If specified, `ebuttm:documentIntendedTargetBarData` SHALL have the attribute `position` specified.||
|R82|3.1.1.1.9|If the `position` attribute has the value `topBottom` then the `ebuttm:documentIntendedTargetBarData` element SHALL also contain the `lineNumberEndOfTopBar` and `lineNumberStartOfBottomBar` attributes.||
|R83|3.1.1.1.9|If the `position` attribute has the value `leftRight` then the `ebuttm:documentIntendedTargetBarData` element SHALL also contain the `pixelNumberEndOfLeftBar` and `pixelNumberStartOfRightBar` attributes.||
|R84|3.1.3.2|`tt:styling` SHALL contain one or more `tt:style` elements||
|R85|3.1.4.2|A style attribute that is defined for `tt:region` SHALL NOT appear in `tt:style` and vice versa. The only exception from this rule is the `tts:padding`, which may appear in both `tt:style` and `tt:region`.||
|R86|3.1.3.2|`tt:div`, `tt:p` and `tt:span` elements SHALL only use references to style definitions.||
|R87|3.1.3.2|The default value of `tts:fontSize` SHALL be `1c` (but `1c 2c` for v1.0)||
|R88|3.1.3.2|The default value of `tts:textAlign` SHALL be `start`||
|R89|3.1.4.2|`tt:layout` SHALL contain one or more `tt:region` elements||
|R90|3.1.4.2|The attributes `tts:origin` and `tts:extent` SHALL be specified on `tt:region`||
|R91|3.1.4.2|If a region exceeds the the boundary of the active video, the display of the region SHALL be clipped.||
|R92|3.1.4.2|The initial value of `tts:displayAlign` SHALL be `before`||
|R93|4.2|Colour values SHALL be constrained to a named colour string, a RGB colour triple, RGBA colour tuple, a hex notated RGB colour triple or a hex notated RGBA colour tuple.|`bdd/features/validation/3350-value-types.feature` `(In)valid colour values`|
|R94|4.3|`extent` values SHALL be constrained to non-negative numbers appended by percentage “%”, c” (for cells) or “px” (for pixels).|`bdd/features/validation/3350-value-types.feature` `(In)valid extent values`|
|R95|4.5|`tts:fontSize` values SHALL be constrained to non-negative numbers appended by “%”, c” or “px”.|`bdd/features/validation/3350-value-types.feature` `(In)valid font size values`|
|R96|4.6|`ttp:frameRateMultiplier` values SHALL be constrained to two positive integers delimited by space|`bdd/features/validation/smpte\_constraints.feature` `(In)valid SMPTE head attributes`|
|R97|4.8|`tts:linePadding` values SHALL be constrained to one non-negative decimal appended by "c" (cell)|`bdd/features/validation/3350-value-types.feature` `(In)valid line padding values`|
|R98|4.9|`tts:lineHeight` values SHALL be constrained to the string `normal` or a non-negative number appended by percentage “%”, c” (for cells) or “px” (for pixels).|`bdd/features/validation/3350-value-types.feature` `(In)valid line height values`|
|R99|4.10|`origin` values SHALL be constrained to two non-negative numbers appended by percentage “%”, c” (for cells) or “px” (for pixels) delimited by a space.|`bdd/features/validation/3350-value-types.feature` `(In)valid origin values`|
|R100|4.11|`tts:padding` values SHALL be constrained to one, two, three or four decimal numbers (`xs:decimal`) appended by percentage “%”, c” (for cells) or “px” (for pixels), delimited by a space.|`bdd/features/validation/padding\_data\_type.feature` `Padding Element and Datatype testing`|
|R101|3.2.2.3.3|`span` `begin` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in span`|
|R102|3.2.2.3.3|`span` `begin` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in span` |
|R103|3.2.2.3.3|`span` `begin` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in span` |
|R104|3.2.2.3.3|`span` `end` attribute: If the timebase is "smpte" the type shall be `ebuttdt:smpteTimingType`. |`bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in span` |
|R105|3.2.2.3.3|`span` `end` attribute: If the timebase is "media" the type shall be `ebuttdt:mediaTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in span`|
|R106|3.2.2.3.3|`span` `end` attribute: If the timebase is "clock" the type shall be `ebuttdt:clockTimingType`. | `bdd/features/validation/timeBase\_timeformat\_constraints.feature` `(In)valid times according to timeBase in span`|
