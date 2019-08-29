from unittest import TestCase
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.node.denester import Denester
from ebu_tt_live.bindings import div_type, p_type, span_type
import re

class TestNester(TestCase):
    # Given a div within a div, only a single div is returned

    def setUp(self):
        xml_file = "testing/bdd/templates/nested_elements_hardcoded.xml"
        with open(xml_file, 'r') as in_file:
           input_xml = in_file.read()
        input_xml = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", input_xml)
        self.actual_doc = EBUTT3Document.create_from_xml(input_xml)
        
        xml_file_2 = "testing/bdd/templates/unnested_elements_hardcoded.xml"
        with open(xml_file_2, 'r') as in_file:
            expected_xml = in_file.read()
        expected_xml = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", expected_xml)
        self.expected_doc = EBUTT3Document.create_from_xml(expected_xml)

        xml_file_3 = "testing/bdd/templates/many_nested_elements_hardcoded.xml"
        with open(xml_file_3, 'r') as in_file:
            input_xml_2 = in_file.read()
        input_xml_2 = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", input_xml_2)
        self.actual_doc_2 = EBUTT3Document.create_from_xml(input_xml_2)

        xml_file_4 = "testing/bdd/templates/many_unnested_elements_hardcoded.xml"
        with open(xml_file_4, 'r') as in_file:
            expected_xml_2 = in_file.read()
        expected_xml_2 = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", expected_xml_2)
        self.expected_doc_2 = EBUTT3Document.create_from_xml(expected_xml_2)

    def test_docs_are_equals(self):
        unnested = self.d.denest(self.actual_doc)
        assert self.expected_doc.get_xml() == unnested.get_xml()
        

    def test_merged_attr_styles_(self):
        excepted_div = self.expected_doc_2.binding.body.div[0]
        actual_div = self.actual_doc_2.binding.body.div[0]
        actual_divs = Denester.denest(actual_div)
        for div in actual_divs:
             assert div.style == excepted_div.style
    

    def test_recurse_one_child_div(self):
        divs =  self.actual_doc.binding.body.div[0]
        expected_div = self.expected_doc.binding.body.div[0]
        actual_div = Denester.recurse(divs)
        print(expected_div.p)
        print(actual_div[0].p)
        assert len(actual_div) == 1
        assert expected_div == actual_div[0]

    def test_recurse_many_child(self):
        expected_divs = self.expected_doc2.binding.body.div
        nested_divs =  self.actual_doc2.binding.body.div
        unnested_divs =  []

        for nested_div in nested_divs:
            unnested_divs.append(Denester.recurse(nested_div))

        assert nested_divs == expected_divs#
   
        
        