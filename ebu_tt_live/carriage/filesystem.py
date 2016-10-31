from .base import ProducerCarriageImpl, ConsumerCarriageImpl
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings import CreateFromDocument
from ebu_tt_live.errors import EndOfData, XMLParsingFailed
from ebu_tt_live.strings import ERR_DECODING_XML_FAILED
from ebu_tt_live.utils import RotatingFileBuffer
from datetime import timedelta
import logging
import os
import time


log = logging.getLogger(__name__)


def timedelta_to_str_manifest(timed, time_base):
    if time_base == 'clock' or time_base == 'media':
        hours, seconds = divmod(timed.seconds, 3600)
        hours += timed.days * 24
        minutes, seconds = divmod(seconds, 60)
        milliseconds, _ = divmod(timed.microseconds, 1000)
        return '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours, minutes, seconds, milliseconds)
    elif time_base == 'smpte':
        raise NotImplementedError()
    else:
        raise ValueError()


def timestr_manifest_to_timedelta(timestr, time_base):
    if time_base == 'clock' or time_base == 'media':
        hours, minutes, rest = timestr.split(":")
        seconds, milliseconds = rest.split(".")
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))
    elif time_base == 'smpte':
        raise NotImplementedError()
    else:
        raise ValueError()


class FilesystemProducerImpl(ProducerCarriageImpl):
    """
    This class implements a carriage mechanism to output produced documents
    to the file system. Its constructor takes a mandatory argument : the path to
    the desired output folder. If the folder does not exist it will be created.
    Each document handled by this carriage implementation is written in an xml file
    in the output folder.
    Along with the xml files, a manifest_sequenceIdentifier.txt file is also written in the output folder.
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
    If the output folder already exists and it contains a manifest_sequenceIdentifier.txt file for the same
    document sequence, the last line of the existing manifest file is parsed to get the last used sequence number
    and the current sequence is set to start from the next sequence number.
    """

    _manifest_path = None
    _dirpath = None
    _manifest_content = None
    _manifest_time_format = None

    def __init__(self, dirpath):
        self._dirpath = dirpath
        if not os.path.exists(self._dirpath):
            os.makedirs(self._dirpath)
        self._manifest_content = ''

    def resume_producing(self):
        manifest_filename = "manifest_" + self._node.document_sequence.sequence_identifier + ".txt"
        self._manifest_path = os.path.join(self._dirpath, manifest_filename)
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
        if self._manifest_path is None:
            manifest_filename = "manifest_" + document.sequence_identifier + ".txt"
            self._manifest_path = os.path.join(self._dirpath, manifest_filename)
        # Handle there the switch and checks to handle the string format to use
        # for times in the manifest file depending on your time base.
        filename = '{}_{}.xml'.format(document.sequence_identifier, document.sequence_number)
        filepath = os.path.join(self._dirpath, filename)
        with open(filepath, 'w') as f:
            f.write(document.get_xml())
        # To be able to format the output we need a datetime.time object and
        # not a datetime.timedelta. The next line serves as a converter (adding
        # a time with a timedelta gives a time)
        time = self._node.reference_clock.get_time()
        time_base = self._node.reference_clock.time_base
        new_manifest_line = '{},{}\n'.format(timedelta_to_str_manifest(time, time_base), filename)
        self._manifest_content += new_manifest_line
        with open(self._manifest_path, 'a') as f:
            f.write(new_manifest_line)


class FilesystemConsumerImpl(ConsumerCarriageImpl):
    """
    This class is responsible for setting the document object from the xml and set its availability time.
    The document is then sent to the node.
    """

    def on_new_data(self, data):
        document = None
        availability_time_str, xml_content = data
        try:
            document = EBUTT3Document.create_from_raw_binding(CreateFromDocument(xml_content))
        except:
            log.exception(ERR_DECODING_XML_FAILED)
            raise XMLParsingFailed(ERR_DECODING_XML_FAILED)

        if document:
            availability_time = timestr_manifest_to_timedelta(availability_time_str, self._node.reference_clock.time_base)
            document.availability_time = availability_time
            self._node.process_document(document)


class FilesystemReader(object):
    """
    This class is responsible for reading the manifest file and sending the corresponding
    availability times and xml file's content to its _custom_consumer. Important note : the
    manifest file and the xml documents have to be in the same folder (it is the default behavior
    of the producer).
    """
    _dirpath = None
    _manifest_path = None
    _custom_consumer = None
    _manifest_time_format = None
    _do_tail = None

    def __init__(self, manifest_path, custom_consumer, do_tail):
        self._dirpath = os.path.dirname(manifest_path)
        self._manifest_path = manifest_path
        self._custom_consumer = custom_consumer
        self._do_tail = do_tail
        with open(manifest_path, 'r') as manifest:
            self._manifest_lines_iter = iter(manifest.readlines())

    def resume_reading(self):
        with open(self._manifest_path, 'r') as manifest_file:
            while True:
                manifest_line = manifest_file.readline()
                if not manifest_line:
                    if self._do_tail:
                        try:
                            time.sleep(0.5)
                        except KeyboardInterrupt:
                            break
                    else:
                        break
                else:
                    availability_time_str, xml_file_name = manifest_line.rstrip().split(',')
                    xml_file_path = os.path.join(self._dirpath, xml_file_name)
                    xml_content = None
                    with open(xml_file_path, 'r') as xml_file:
                        xml_content = xml_file.read()
                    data = [availability_time_str, xml_content]
                    self._custom_consumer.on_new_data(data)


class SimpleFolderExport(ProducerCarriageImpl):

    _dir_path = None
    _file_name_pattern = None
    _counter = None

    def __init__(self, dir_path, file_name_pattern):
        if not os.path.exists(dir_path):
            raise Exception('Directory: {} could not be found.'.format(dir_path))
        self._dir_path = dir_path
        self._file_name_pattern = file_name_pattern
        self._counter = 0

    def _do_write_document(self, document):
        self._counter += 1
        filename = self._file_name_pattern.format(self._counter)
        filepath = os.path.join(self._dir_path, filename)
        with open(filepath, 'w') as destfile:
            destfile.write(document.get_xml())
            destfile.flush()
        return filepath

    def emit_document(self, document):
        self._do_write_document(document)


class RotatingFolderExport(SimpleFolderExport):

    _circular_buf = None

    def __init__(self, dir_path, file_name_pattern, circular_buf_size):
        super(RotatingFolderExport, self).__init__(dir_path, file_name_pattern)
        self._circular_buf = RotatingFileBuffer(maxlen=circular_buf_size)

    def emit_document(self, document):
        file_name = self._do_write_document(document)
        self._circular_buf.append(file_name)
