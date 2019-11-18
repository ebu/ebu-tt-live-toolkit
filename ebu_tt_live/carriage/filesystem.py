from .base import AbstractProducerCarriage, AbstractConsumerCarriage
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.errors import EndOfData
from ebu_tt_live.clocks import get_clock
from ebu_tt_live.utils import RotatingFileBuffer
from ebu_tt_live.strings import FS_DEFAULT_CLOCK_USED, FS_MISSING_AVAILABILITY, CFG_FILENAME_PATTERN, CFG_MESSAGE_PATTERN, CFG_MANIFEST_FILENAME_PATTERN, CFG_MANIFEST_LINE_PATTERN
from datetime import timedelta
import logging
import six
import os
import time
import codecs


log = logging.getLogger(__name__)


def timedelta_to_str_manifest(timed):
        hours, seconds = divmod(timed.seconds, 3600)
        hours += timed.days * 24
        minutes, seconds = divmod(seconds, 60)
        milliseconds, _ = divmod(timed.microseconds, 1000)
        return '{:02d}:{:02d}:{:02d}.{:03d}'.format(hours, minutes, seconds, milliseconds)


def timestr_manifest_to_timedelta(timestr):
        hours, minutes, rest = timestr.split(":")
        seconds, milliseconds = rest.split(".")
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

# NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.

class FilesystemProducerImpl(AbstractProducerCarriage):
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
    _file_name_pattern = None
    _message_file_name_pattern = None
    _manifest_time_format = None
    _circular_buf_size = 0
    _circular_buf = None
    _counter = None
    _suppress_manifest = False
    _expects = six.text_type
    _default_clocks = None
    _msg_counter = None

    def __init__(self, 
                 dirpath, 
                 file_name_pattern = CFG_FILENAME_PATTERN, 
                 message_file_name_pattern = CFG_MESSAGE_PATTERN, 
                 circular_buf_size = 0, 
                 suppress_manifest = False,
                 first_msg_counter = 0):
        self._dirpath = dirpath
        if not os.path.exists(self._dirpath):
            os.makedirs(self._dirpath)
        self._file_name_pattern = file_name_pattern
        self._message_file_name_pattern = message_file_name_pattern
        self._counter = 0
        self._msg_counter = first_msg_counter
        self._circular_buf_size = circular_buf_size
        if circular_buf_size > 0 :
            self._circular_buf = RotatingFileBuffer(maxlen=circular_buf_size)
        self._suppress_manifest = suppress_manifest
        # Get a set of default clocks
        self._default_clocks = {}

    def _get_default_clock(self, sequence_identifier, time_base, clock_mode=None):
        clock_obj = self._default_clocks.get(sequence_identifier, None)
        if clock_obj is None:
            clock_obj = get_clock(time_base=time_base, clock_mode=clock_mode)
            if clock_obj is not None:
                log.warning(FS_DEFAULT_CLOCK_USED.format(sequence_identifier=sequence_identifier))
                self._default_clocks[sequence_identifier] = clock_obj
        return clock_obj

    def set_message_counter(self, message_counter):
        self._msg_counter = message_counter
        
    def check_availability_time(
            self, sequence_identifier, time_base=None, clock_mode=None, availability_time=None):
        """
        Make sure we have a suitable timedelta value sent down from upstream as availability_time.
        If the value is None or unusable use the default clock to derive an availability time
        for the current document. (This does not check if the value is within valid range)

        :param sequence_identifier: remember default clock used per sequence
        :param time_base: document time base
        :param clock_mode: in clock timebase this parameter is needed
        :param availability_time: provided availability_time from upstream
        :return: a valid availability_time (timedelta)

        """

        if not isinstance(availability_time, timedelta):
            availability_time = None
            # If availability time is not provided a default clock should be used
            clock_obj = self._get_default_clock(
                sequence_identifier=sequence_identifier, time_base=time_base, clock_mode=clock_mode
            )
            if clock_obj is not None:
                availability_time = clock_obj.get_real_clock_time()

        return availability_time

    def resume_producing(self):
        while True:
            try:
                self.producer_node.resume_producing()
            except EndOfData:
                break

    def emit_data(self, data, sequence_identifier=None, sequence_number=None,
                  time_base=None, availability_time=None, delay=None, clock_mode=None, **kwargs):

        # Handle there the switch and checks to handle the string format to use
        # for times in the manifest file depending on your time base.
        if sequence_number is None:
            # This means that it isn't a Part 3 document. It can be a message, or an EBU-TT-D document.
            # We don't try to spot the difference between a message and an EBU-TT-D document:
            # instead we just use the message format for EBU-TT-D documents!
            self._msg_counter += 1
            filename = self._message_file_name_pattern.format(
                counter=self._msg_counter, 
                sequence_identifier=sequence_identifier)
        else:
            # It's a Part 3 document, so use the sequence number.
            filename = self._file_name_pattern.format(
                counter=sequence_number, 
                sequence_identifier=sequence_identifier)
            
        # TODO: consider using different classes or functions to do the document writing,
        # depending on the settings of suppress_manifest and rotating_buf etc that
        # can be selected once at the beginning and dereferenced rather than repeating
        # if statements.
        filepath = os.path.join(self._dirpath, filename)
        with codecs.open(filepath, mode='w', errors='ignore') as destfile:
            destfile.write(data)
            destfile.flush()
                        
        # If we're running a rotating buffer remember this file for possible deletion later
        if self._circular_buf_size > 0 :
            self._circular_buf.append(filepath)
            
        if not self._suppress_manifest :
            # Work out what time to put in the manifest file
            
            # NOTE: This is nasty
            availability_time = self.check_availability_time(
                sequence_identifier=sequence_identifier,
                time_base=time_base,
                clock_mode=clock_mode,
                availability_time=availability_time
            )

            if availability_time is None:
                # This is a possibility with a live messages as first document.
                # They don't contain enough timing info.
                log.warning(
                    FS_MISSING_AVAILABILITY.format(
                        sequence_identifier=sequence_identifier,
                        file_path=filepath)
                )
                # Without availability time we can not create manifest file.
                # In this case we have written an output file but no matching
                # entry in the manifest file.
                return

            if delay is not None:
                availability_time += timedelta(seconds=delay)

            # Open the manifest filepath
            if self._manifest_path is None :
                manifest_filename = CFG_MANIFEST_FILENAME_PATTERN.format(
                    sequence_identifier=sequence_identifier)
                self._manifest_path = os.path.join(self._dirpath, manifest_filename)
                
            # Write a new line to the manifest file
            new_manifest_line = CFG_MANIFEST_LINE_PATTERN.format(
                availability_time=timedelta_to_str_manifest(availability_time), 
                filename=filename)
            with codecs.open(self._manifest_path, mode='a', errors='ignore') as f:
                f.write(new_manifest_line)


class FilesystemConsumerImpl(AbstractConsumerCarriage):
    """
    This class is responsible for setting the document object from the xml and set its availability time.
    The document is then sent to the node.
    """

    _provides = six.text_type

    def on_new_data(self, data, **kwargs):
        availability_time_str, xml_content = data

        if xml_content:
            availability_time = timestr_manifest_to_timedelta(availability_time_str)
            self.consumer_node.process_document(xml_content, availability_time=availability_time)


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
        with codecs.open(manifest_path, 'r') as manifest:
            self._manifest_lines_iter = iter(manifest.readlines())

    def resume_reading(self):
        with codecs.open(self._manifest_path, 'r') as manifest_file:
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
                    # If CFG_MANIFEST_LINE_PATTERN changes, then the parsing below needs to change too.
                    availability_time_str, xml_file_name = manifest_line.rstrip().split(',')
                    xml_file_path = os.path.join(self._dirpath, xml_file_name)
                    xml_content = None
                    with codecs.open(xml_file_path, 'r') as xml_file:
                        xml_content = xml_file.read()
                    data = [availability_time_str, xml_content]
                    self._custom_consumer.on_new_data(data)
