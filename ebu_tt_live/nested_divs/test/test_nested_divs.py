from unittest import TestCase
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.node.denester import Denester
import re

class TestNester(TestCase):
    # Given a div within a div, only a single div is returned
    def test_docs_are_equals(self):
        xml_file = "testing/bdd/templates/nested_elements_hardcoded.xml"
        xml_file_2 = "testing/bdd/templates/unnested_elements_hardcoded.xml"
        expected = None #put expected ebutt here

        with open(xml_file, 'r') as in_file:
            input_xml = in_file.read()

        input_xml = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", input_xml)
        ebutt3 = EBUTT3Document.create_from_xml(input_xml)

        with open(xml_file_2, 'r') as in_file:
            expected_xml = in_file.read()
        
        expected_xml = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", expected_xml)
        expected = EBUTT3Document.create_from_xml(expected_xml)


        unnested = Denester.denest(ebutt3)

        assert expected.get_xml() == unnested.get_xml()

    def test_style_merge_from_parent(self):
        expected_styles = {"styles": ["s1","s2"]}
        assert expected_styles == Denester.setup_properties(expected_styles, None, None, None, None)