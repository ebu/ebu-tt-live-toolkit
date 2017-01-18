
from unittest import TestCase
from mock import MagicMock
import tempfile
from ebu_tt_live.utils import RingBufferWithCallback, RotatingFileBuffer, RotatingFileBufferStopped
import os
import time


class TestRingBuffer(TestCase):

    maxlen = 3

    def setUp(self):
        self.callback = MagicMock()
        self.instance = RingBufferWithCallback(
            maxlen=self.maxlen,
            callback=self.callback
        )

    def test_add_one_item(self):
        self.instance.append(1)
        self.callback.assert_not_called()

    def test_add_three_items(self):
        self.instance.append(1)
        self.instance.append(2)
        self.instance.append(3)
        self.callback.assert_not_called()

    def test_add_four_items(self):
        self.test_add_three_items()
        self.instance.append(4)
        self.callback.assert_called_with(1)

    def test_add_five_items(self):
        self.test_add_four_items()
        self.instance.append(5)
        self.callback.assert_called_with(2)


class RFBCommon(TestCase):

    def setUp(self):
        self.files_created = []

    def tearDown(self):
        for item in self.files_created:
            if os.path.exists(item):
                os.remove(item)

    def _create_a_file(self, number):
        created_file = tempfile.NamedTemporaryFile(
            prefix='ebu_tt_live_utils_test',
            suffix='{}.tmp'.format(number),
            delete=False
        )
        created_file.file.write('TestFile {}'.format(number))
        created_file.file.close()
        file_name = created_file.name
        # Adding it to the cleanup
        self.files_created.append(file_name)
        # OK we closed the file let's make sure it is still on the system
        self._assert_exists(file_name)
        return file_name

    def _assert_exists(self, file_name):
        self.assertTrue(os.path.exists(file_name))

    def _assert_not_exists(self, file_name):
        self.assertFalse(os.path.exists(file_name))


class TestRotatingFileBufferSync(RFBCommon):

    def setUp(self):
        super(TestRotatingFileBufferSync, self).setUp()
        self.instance = RotatingFileBuffer(maxlen=3, async=False)

    def test_one_file(self):
        file1 = self._create_a_file(1)
        self.instance.append(file1)
        self._assert_exists(file1)

    def test_three_files(self):
        file1 = self._create_a_file(1)
        file2 = self._create_a_file(2)
        file3 = self._create_a_file(3)
        self.instance.append(file1)
        self.instance.append(file2)
        self.instance.append(file3)
        self._assert_exists(file1)
        self._assert_exists(file2)
        self._assert_exists(file3)

    def test_four_files(self):
        file1 = self._create_a_file(1)
        file2 = self._create_a_file(2)
        file3 = self._create_a_file(3)
        file4 = self._create_a_file(4)
        self.instance.append(file1)
        self.instance.append(file2)
        self.instance.append(file3)
        self.instance.append(file4)

        self._assert_not_exists(file1)
        self._assert_exists(file2)
        self._assert_exists(file3)
        self._assert_exists(file4)


class TestRotatingFileBufferAsync(RFBCommon):

    def setUp(self):
        super(TestRotatingFileBufferAsync, self).setUp()
        self.instance = RotatingFileBuffer(maxlen=3)

    def _stop_thread(self):
        if not self.instance._deletion_thread.stopped():
            self.instance._deletion_thread.stop()
            self.instance._deletion_thread.join()

    def test_one_file(self):
        file1 = self._create_a_file(1)
        self.instance.append(file1)
        self._stop_thread()
        self._assert_exists(file1)

    def test_four_files(self):
        file1 = self._create_a_file(1)
        file2 = self._create_a_file(2)
        file3 = self._create_a_file(3)
        file4 = self._create_a_file(4)
        self.instance.append(file1)
        self.instance.append(file2)
        self.instance.append(file3)
        self.instance.append(file4)
        self._stop_thread()
        self._assert_not_exists(file1)
        self._assert_exists(file2)
        self._assert_exists(file3)
        self._assert_exists(file4)

    def test_late_insertion(self):
        file1 = self._create_a_file(1)
        file2 = self._create_a_file(2)
        self.instance.append(file1)
        self._stop_thread()
        self.assertRaises(RotatingFileBufferStopped, self.instance.append, file2)

    def tearDown(self):
        self._stop_thread()
        super(TestRotatingFileBufferAsync, self).tearDown()
