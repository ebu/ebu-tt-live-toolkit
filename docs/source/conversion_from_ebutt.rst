Conversion of EBU-TT Part 1 documents to EBU-TT Live documents
==============================================================

The :py:func:`ebu_tt_live.documents.converters.ebutt1_to_ebutt3` function
creates an EBUTT3Document from an EBUTT1Document using the helper class
:py:class:`ebu_tt_live.bindings.converters.ebutt1_ebutt3.EBUTT1EBUTT3Converter`.

This class manages various possible complications, including mapping SMPTE
timecodes into media time, and setting a sequence identifier. 

Here's some documentation from the coding process that captures some of our
internal conversation about how to map font sizes, to give an idea of the
complexity.

The problem
-----------

Convert an EBU-TT part 1 document to an EBU-TT part 3 document

EBU-TT part 1 can have smpte timebase; EBU-TT part 3 cannot.
EBU-TT part 1 must not have a sequence identifier and must not
have a sequence number. EBU-TT part 3 documents must have both.

In order to set the sequence identifier the converter can be
configured with the desired value, or it can be set to extract the
document identifier from the ``ebuttm:documentIdentifier`` element
and use it, if it exists.

If the EBU-TT part 1 document uses the ``smpte`` timebase, then all
the time expressions must be converted to some other timebase.
Currently they are all converted to ``media``, using a simple fixed
offset based conversion strategy, encapsulated in the utility class
:py:class:`ebu_tt_live.bindings.converters.timedelta_converter.FixedOffsetSMPTEtoTimedeltaConverter`. 
This currently looks for the metadata attribute 
``tt/head/metadata/ebuttm:documentMetadata/ebuttm:documentStartOfProgramme``
and if it finds it, uses that as
the zero point, otherwise it uses ``00:00:00:00``. This can be
overridden by setting the ``smpte_start_of_programme`` parameter to the
start of programme timecode to use instead.

The document's frame rate, frame rate multiplier and drop mode are taken into
account when doing the conversion. This means that illegal frame
values will cause a
:py:class:`ebu_tt_live.errors.TimeFormatError` exception to be raised.

Elements with ``begin`` or ``end`` attributes that fall before the start of
programme are discarded.
