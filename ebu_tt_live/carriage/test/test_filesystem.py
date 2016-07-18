from unittest import TestCase
from mock import patch, MagicMock
from ebu_tt_live.carriage import FilesystemProducerImpl, FilesystemConsumerImpl, FilesystemReader, MANIFEST_TIME_CLOCK_FORMAT
from ebu_tt_live.errors import XMLParsingFailed
import os
import tempfile
import shutil
import datetime


class TestFilesystemProducerImpl(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_dir_path = os.path.abspath(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_instantiation(self):
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        self.assertIsInstance(fs_carriage, FilesystemProducerImpl)

    @patch('ebu_tt_live.node.SimpleProducer')
    def test_resume_producing(self, node):
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        node.process_document = MagicMock(return_value=False)
        fs_carriage.register(node)
        fs_carriage.resume_producing()
        assert node.process_document.called
        manifest_path = os.path.join(self.test_dir_path, 'manifest.txt')
        assert os.path.exists(manifest_path)

    def test_emit_document(self):
        document = MagicMock(sequence_identifier="testSeq", sequence_number=1)
        document.get_xml = MagicMock(return_value="test")
        node = MagicMock()
        node.reference_clock.get_time().return_value = 1
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        fs_carriage.register(node)
        fs_carriage.emit_document(document)
        exported_document_path = os.path.join(self.test_dir_path, 'testSeq_1.xml')
        assert os.path.exists(exported_document_path)


class TestFilesystemConsumerImpl(TestCase):

    def setUp(self):
        self.test_data_dir_path = os.path.join(os.path.dirname(__file__), 'test_data')

    @patch('ebu_tt_live.node.SimpleConsumer')
    def test_on_new_data(self, node):
        node.process_document = MagicMock(return_value=True)
        test_xml = None
        test_xml_file_path = os.path.join(self.test_data_dir_path, 'TestSequence1_1.xml')
        with open(test_xml_file_path, 'r') as test_xml_file:
            test_xml = test_xml_file.read()
        data = ["18:42:42.42", test_xml]
        fs_consumer_impl = FilesystemConsumerImpl()
        fs_consumer_impl.register(node)
        fs_consumer_impl.on_new_data(data)
        assert node.process_document.called

    @patch('ebu_tt_live.node.SimpleConsumer')
    def test_on_new_data_raise_XMLParsingFailed(self, node):
        node.process_document = MagicMock(return_value=None)
        data = ["18:42:42.42", "test"]
        fs_consumer_impl = FilesystemConsumerImpl()
        fs_consumer_impl.register(node)
        self.assertRaises(XMLParsingFailed, lambda: fs_consumer_impl.on_new_data(data))
        assert not node.process_document.called


class TestFilesystemReader(TestCase):

    def setUp(self):
        self.test_data_dir_path = os.path.join(os.path.dirname(__file__), 'test_data')

    @patch('ebu_tt_live.carriage.FilesystemConsumerImpl')
    def test_resume_reading(self, fs_carriage_impl):
        fs_carriage_impl.on_new_data = MagicMock(return_value=None)
        fs_reader = FilesystemReader(self.test_data_dir_path, fs_carriage_impl)
        test_manifest_path = os.path.join(self.test_data_dir_path, 'manifest.txt')
        test_xml = None
        availability_time = None
        with open(test_manifest_path, 'r') as test_manifest:
            manifest_line = test_manifest.readline()
            availability_time_str, test_xml_file_name = manifest_line.rstrip().split(',')
            availability_time = datetime.datetime.strptime(availability_time_str, MANIFEST_TIME_CLOCK_FORMAT).time()
            test_xml_file_path = os.path.join(self.test_data_dir_path, test_xml_file_name)
            with open(test_xml_file_path, 'r') as test_xml_file:
                test_xml = test_xml_file.read()
        fs_reader.resume_reading()
        data = [availability_time, test_xml]
        fs_carriage_impl.on_new_data.assert_called_once_with(data)

