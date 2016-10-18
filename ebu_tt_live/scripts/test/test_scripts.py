
from subprocess import Popen, PIPE
from unittest import TestCase
from ebu_tt_live.scripts import ebu_dummy_encoder


class TestDummyScript(TestCase):

    def test_simple_run(self):
        process = Popen('ebu-dummy-encoder', stderr=PIPE, stdout=PIPE)
        process.communicate()
        self.assertEquals(process.returncode, 0)
