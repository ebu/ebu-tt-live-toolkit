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
    def test_resume_producing(self, node):
        fs_carriage = FilesystemProducerImpl(self.test_dir_path)
        node.process_document = MagicMock(side_effect=EndOfData())
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
