from unittest import TestCase
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from ebu_tt_live.carriage import FileSystemCarriageImpl
import os
import tempfile
import shutil


class TestFileSystemCarriageImpl(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_instantiation(self):
        fs_carriage = FileSystemCarriageImpl(os.path.abspath(self.test_dir))
        self.assertIsInstance(fs_carriage, FileSystemCarriageImpl)

    @patch('ebu_tt_live.node.SimpleProducer')
    def test_resume_producing(self, simpleProducer):
        fs_carriage = FileSystemCarriageImpl(os.path.abspath(self.test_dir))
        simpleProducer.process_document = MagicMock(return_value=False)
        fs_carriage.register(simpleProducer)
        fs_carriage.resume_producing()
        assert simpleProducer.process_document.called
        manifest_path = os.path.join(os.path.abspath(self.test_dir), 'manifest.txt')
        assert os.path.exists(manifest_path)
