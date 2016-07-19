from .base import ProducerCarriageImpl, ConsumerCarriageImpl
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings import CreateFromDocument
from ebu_tt_live.strings import ERR_DECODING_XML_FAILED
from ebu_tt_live.errors import XMLParsingFailed, EndOfData
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
    The writing order and thus the reading order is from top to bottom. Please note that depending
    on the clock used by the producer node, time may loop (going to the next day), this is especially
    the case with `ttp:timeBase="clock"`.
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
        while True:
            try:
                self._node.process_document(document=None)
            except EndOfData:
                break
        self.write_manifest()

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
        self._manifest_content += '{},{}\n'.format(time.strftime(self._manifest_time_format), filename)

    def write_manifest(self):
        self._manifest_file = open(self._manifest_path, 'w')
        self._manifest_file.write(self._manifest_content)
        self._manifest_file.close()


class FilesystemConsumerImpl(ConsumerCarriageImpl):
    """
    This class is where the logic for availability times should be implemented. This allows us to implement different
    interpretation of availability times by simply adding new CarriageMechanism, the reading of the files itself being
    done in ebutt_live.carriage.FilesystemReader file.
    """

    def on_new_data(self, data):
        document = None
        availability_time, xml_content = data
        try:
            document = EBUTT3Document.create_from_raw_binding(CreateFromDocument(xml_content))
        except:
            log.exception(ERR_DECODING_XML_FAILED)
            raise XMLParsingFailed(ERR_DECODING_XML_FAILED)

        if document:
            self._node.process_document(document)


class FilesystemReader(object):
    """
    This class is responsible for reading the manifest file and sending the corresponding
    availability times and xml file's content to its _custom_consumer.
    """
    _dirpath = None
    _manifest_lines_iter = None
    _custom_consumer = None
    _manifest_time_format = None

    def __init__(self, dirpath, custom_consumer):
        self._dirpath = dirpath
        self._custom_consumer = custom_consumer
        manifest_path = os.path.join(dirpath, 'manifest.txt')
        with open(manifest_path, 'r') as manifest:
            self._manifest_lines_iter = iter(manifest.readlines())

    def resume_reading(self):
        if not self._manifest_time_format:
            self._manifest_time_format = MANIFEST_TIME_CLOCK_FORMAT
        manifest_line = None
        try:
            manifest_line = self._manifest_lines_iter.next()
        except StopIteration:
            raise EndOfData
        availability_time_str, xml_file_name = manifest_line.rstrip().split(',')
        availability_time = datetime.datetime.strptime(availability_time_str, MANIFEST_TIME_CLOCK_FORMAT).time()
        xml_file_path = os.path.join(self._dirpath, xml_file_name)
        xml_content = None
        with open(xml_file_path, 'r') as xml_file:
            xml_content = xml_file.read()
        data = [availability_time, xml_content]
        self._custom_consumer.on_new_data(data)
