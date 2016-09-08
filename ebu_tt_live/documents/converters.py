
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.ebuttd import EBUTTDDocument
from subprocess import Popen, PIPE
import tempfile
import os
import logging


log = logging.getLogger(__name__)


def ebutt3_to_ebuttd(ebutt3_in, media_clock):
    """
    This function takes an EBUTT3Document instance and returns the same document as an EBUTTDDocument instance.
    :param ebutt3_in:
    :return:
    """
    converter = EBUTT3EBUTTDConverter(media_clock=media_clock)
    ebuttd_bindings = converter.convert_element(ebutt3_in.binding, dataset={})
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
    ebuttd_document.validate()
    return ebuttd_document


class MP4BoxConverter(object):

    _dir_path = None
    _file_name_pattern = None
    _counter = None

    def __init__(self, dir_path, file_name_pattern):
        if not os.path.exists(dir_path):
            raise Exception('Directory: {} could not be found.'.format(dir_path))
        self._dir_path = dir_path
        self._file_name_pattern = file_name_pattern
        self._counter = 0

    def emit_document(self, document):
        docnumber = self._counter
        self._counter += 1
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xml')
        temp_file.write(document.get_xml())
        temp_file.flush()
        temp_file.close()
        process = Popen(
            [
                'MP4Box',
                '-add',
                '{}:ext=ttml'.format(temp_file.name),
                '-new',
                os.path.join(self._dir_path, self._file_name_pattern.format(docnumber))
            ],
            stdout=PIPE,
            stderr=PIPE
        )
        stdout, stderr = process.communicate()
        log.info(stdout)
        log.info(stderr)



