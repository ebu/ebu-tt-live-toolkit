from .base import ProducerCarriageImpl
from ebu_tt_live.errors import EndOfData
import logging
import os
import datetime

MANIFEST_TIME_CLOCK_FORMAT = '%H:%M:%S.%f'

log = logging.getLogger(__name__)


class FilesystemProducerImpl(ProducerCarriageImpl):
    """
    This class implements a carriage mechanism to output produced documents
    to the file system. Its constructor takes a mandatory argument : the path to
    the desired output folder. If the folder does not exist it will be created.
    Each document handled by this carriage implementation is written in an xml file
    in the output folder.
    Along with the xml files, a manifest.txt file is also written in the output folder.
    Each time an xml file is written, a line using the following format is added to the manifest :

    `availability_time,path_to_xml_file`

    The manifest file gives the availability time for each document along with the path to the
    corresponding document.
    The timeline used for the availability times is the same as the one used in the documents,
    indeed the carriage implementation uses the same clock (or time reference) as the node that
    produces the documents.
    The writing order and thus the reading order is from top to bottom. Please note that depending on the
    timebase used by the producer node time may loop (going to the next day). It can loop with
    `ttp:timeBase="clock"` or `ttp:timeBase="smpte"`, but not with `ttp:timeBase="media"`.
    """

    _manifest_path = None
    _dirpath = None
    _manifest_file = None
    _manifest_content = None
    _manifest_time_format = None

    def __init__(self, dirpath):
        self._dirpath = dirpath
        if not os.path.exists(self._dirpath):
            os.makedirs(self._dirpath)
        self._manifest_path = os.path.join(dirpath, 'manifest.txt')
        self._manifest_content = ''

    def resume_producing(self):
        if os.path.exists(self._manifest_path):
            with open(self._manifest_path, 'r') as f:
                for last_line in f:
                    pass
                # Line has format: time,filename
                # Where filename has the format:
                # sequenceIdentifier_sequenceNumber.xml
                _, last_filename = last_line.split(',')
                last_sequence_number, _ = last_filename.split('_')[1].split('.')
                self._node.document_sequence.last_sequence_number = int(last_sequence_number)
        while True:
            try:
                self._node.process_document(document=None)
            except EndOfData:
                break

    def emit_document(self, document):
        # Handle there the switch and checks to handle the string format to use
        # for times in the manifest file depending on your time base.
        if not self._manifest_time_format:
            self._manifest_time_format = MANIFEST_TIME_CLOCK_FORMAT
        filename = '{}_{}.xml'.format(document.sequence_identifier, document.sequence_number)
        filepath = os.path.join(self._dirpath, filename)
        with open(filepath, 'w') as f:
            f.write(document.get_xml())
        # To be able to format the output we need a datetime.time object and
        # not a datetime.timedelta. The next line serves as a converter (adding
        # a time with a timedelta gives a time)
        time = (datetime.datetime.min + self._node.reference_clock.get_time()).time()
        new_manifest_line = '{},{}\n'.format(time.strftime(self._manifest_time_format), filename)
        self._manifest_content += new_manifest_line
        with open(self._manifest_path, 'a') as f:
            f.write(new_manifest_line)
