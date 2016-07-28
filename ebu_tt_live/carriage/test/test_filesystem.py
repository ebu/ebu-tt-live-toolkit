from unittest import TestCase
from mock import patch, MagicMock
from ebu_tt_live.carriage.filesystem import FilesystemProducerImpl
from ebu_tt_live.errors import EndOfData
import os
import tempfile
import shutil


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
    def test_resume_producing_no_existing_manifest(self, node):
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        node.process_document = MagicMock(side_effect=EndOfData())
        node.document_sequence.sequence_identifier = "testSeq"
        fs_carriage.register(node)
        fs_carriage.resume_producing()
        assert node.process_document.called

    @patch('ebu_tt_live.node.SimpleProducer')
    def test_resume_producing_existing_manifest(self, node):
        manifest_path = os.path.join(self.test_dir_path, "manifest_testSeq.txt")
        with open(manifest_path, 'w') as f:
            f.write("00:00:00.123678,testSeq_177.xml")
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        node.process_document = MagicMock(side_effect=EndOfData())
        node.document_sequence.sequence_identifier = "testSeq"
        fs_carriage.register(node)
        fs_carriage.resume_producing()
        assert node.process_document.called
        self.assertEqual(node.document_sequence.last_sequence_number, 177)

    def test_emit_document(self):
        document = MagicMock(sequence_identifier="testSeq", sequence_number=1)
        document.get_xml = MagicMock(return_value="test")
        node = MagicMock()
        node.reference_clock.get_time().return_value = 1
        node.process_document = MagicMock(side_effect=EndOfData())
        node.document_sequence.sequence_identifier = "testSeq"
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        fs_carriage.register(node)
        fs_carriage.resume_producing()
        fs_carriage.emit_document(document)
        exported_document_path = os.path.join(self.test_dir_path, 'testSeq_1.xml')
        assert os.path.exists(exported_document_path)
        manifest_path = os.path.join(self.test_dir_path, 'manifest_testSeq.txt')
        assert os.path.exists(manifest_path)
