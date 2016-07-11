from unittest import TestCase
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
