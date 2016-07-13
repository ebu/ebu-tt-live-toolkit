from ebu_tt_live.node import ProducerCarriageImpl
import os
import datetime


class FileSystemProducerImpl(ProducerCarriageImpl):

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

