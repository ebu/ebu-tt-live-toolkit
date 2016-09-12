
from gettext import gettext

# ERRORS
ERR_CONV_NO_INPUT = gettext('The converter has no input set')
ERR_TIME_WRONG_FORMAT = gettext('Wrong time format. datetime.timedelta is expected')
ERR_TIME_FORMAT_OVERFLOW = gettext('Time value is out of format range')
ERR_DOCUMENT_SEQUENCE_MISMATCH = gettext('sequenceIdentifier mismatch')
ERR_DECODING_XML_FAILED = gettext('XML document parsing failed')
ERR_SEMANTIC_VALIDATION_TIMING_TYPE = gettext('{attr_type}({attr_value}) is not a valid type for {attr_name} in timeBase={time_base}')
ERR_SEMANTIC_VALIDATION_MISSING_ATTRIBUTES = gettext('{elem_name} is missing attributes: {attr_names}')
ERR_SEMANTIC_VALIDATION_INVALID_ATTRIBUTES = gettext('{elem_name} has invalid attributes: {attr_names}')
ERR_DOCUMENT_NOT_COMPATIBLE = gettext('Document is not compatible with the sequence. Conflicting attributes: {attr_names}')
ERR_SEQUENCE_NUMBER_ALREADY_USED = gettext('The sequence number of the new document has already been used in the sequence.')
ERR_DOCUMENT_NOT_PART_OF_SEQUENCE = gettext('Document is not part of any sequence')
ERR_DOCUMENT_SEQUENCE_INCONSISTENCY = gettext('Timeline consistency problem.')
ERR_DOCUMENT_EXTENT_MISSING = gettext('{type} cannot be instantiated from {value} because document extent is missing (from the tt element)')
END_OF_DATA = gettext('End of available data reached')


DOC_SYNTACTIC_VALIDATION_SUCCESSFUL = gettext('Syntactic validation successful')
DOC_SEMANTIC_VALIDATION_SUCCESSFUL = gettext('Semantic validation successful')
DOC_DISCARDED = gettext('Document {sequence_identifier}__{sequence_number} is discarded')
DOC_TRIMMED = gettext('Document {sequence_identifier}__{sequence_number} activation change: [{resolved_begin_time}; {resolved_end_time}]')
DOC_RECEIVED = gettext('Document {sequence_identifier}__{sequence_number} received. Calculated activation: [{computed_begin_time}; {computed_end_time}]')
