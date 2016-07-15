from ebu_tt_live.node import ProducerCarriageImpl, ConsumerCarriageImpl
import os
import datetime


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

    def __init__(self, dirpath):
        self._dirpath = dirpath
        if not os.path.exists(self._dirpath):
            os.makedirs(self._dirpath)
        self._manifest_path = os.path.join(dirpath, 'manifest.txt')
        self._manifest_content = ''

    def resume_producing(self):
        # None, since this is a producer module. It will produce a new document.
        while self._node.process_document(document=None):
            pass
        self.write_manifest()

    def emit_document(self, document):
        filename = '{}_{}.xml'.format(document.sequence_identifier, document.sequence_number)
        filepath = os.path.join(self._dirpath, filename)
        with open(filepath, 'w') as f:
            f.write(document.get_xml())
        # To be able to format the output we need a datetime.time object and
        # not a datetime.timedelta. The next line serves as a converter (adding
        # a time with a timedelta gives a time)
        time = (datetime.datetime.min + self._node.reference_clock.get_time()).time()
        self._manifest_content += '{},{}\n'.format(time.strftime('%H:%M:%S.%f'), filename)

    def write_manifest(self):
        self._manifest_file = open(self._manifest_path, 'w')
        self._manifest_file.write(self._manifest_content)
        self._manifest_file.close()


class FilesystemConsumerImpl(ConsumerCarriageImpl):

    def on_new_data(self, data):
        raise NotImplementedError()

