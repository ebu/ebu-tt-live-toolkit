Segmentation of EBU-TT-Live document sequences
==============================================

Document sequences may contain arbitrary length of documents with irregular issue times. Some output formats or
carriage mechanisms may require a regular issuing schedule of documents (i.e. every 2 seconds). Therefore the live
sequence supports resegmentation of the subtitle stream into blocks required by the user. The sequence object
has the :py:func:`ebu_tt_live.documents.ebutt3.EBUTT3DocumentSequence.extract_segment` function that looks up the
internal timeline to find any documents that intersect the requested range and in turn calls
:py:func:`ebu_tt_live.documents.ebutt3.EBUTT3Document.extract_segment` on each of them
using :py:class:`ebu_tt_live.documents.ebutt3_segmentation.EBUTT3Segmenter` and merge the resulting
documents into one EBUTT3Document in the end using :py:class:`ebu_tt_live.documents.ebutt3_splicer.EBUTT3Splicer`
After that these documents can be converted to EBU-TT-D for instance to be embedded into DASH,
which requires such a regular document issuing strategy.
