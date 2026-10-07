
from subprocess import PIPE, Popen
from unittest import TestCase


class TestDummyScript(TestCase):

    def test_simple_run(self):
        process = Popen('ebu-dummy-encoder', stderr=PIPE, stdout=PIPE)
        process.communicate()
        self.assertEqual(process.returncode, 0)
