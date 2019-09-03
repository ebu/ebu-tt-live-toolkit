from unittest import TestCase
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.node.denester import Denester
from ebu_tt_live.bindings import div_type, p_type, span_type
from ebu_tt_live.bindings._ebuttm import divMetadata_type
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

        xml_file_5 = "testing/bdd/templates/regions_nested_elements_hardcoded.xml"
        with open(xml_file_5, 'r') as in_file:
            input_xml_3 = in_file.read()
        input_xml_3 = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", input_xml_3)
        self.actual_doc_3 = EBUTT3Document.create_from_xml(input_xml_3)

        xml_file_6 = "testing/bdd/templates/regions_unnested_elements_hardcoded.xml"
        with open(xml_file_6, 'r') as in_file:
            expected_xml_3 = in_file.read()
        expected_xml_3 = re.sub(r"(<ebuttm:documentStartOfProgramme>[^<]*</ebuttm:documentStartOfProgramme>)", r"<!-- \1 -->", expected_xml_3)
        self.expected_doc_3 = EBUTT3Document.create_from_xml(expected_xml_3)
        

    def test_merged_attr_styles_(self):
        excepted_div_attr = {
            "styles" : ["S1","S2"],
        }
        parent_attr = {
            "styles" : ["S2"],
            "lang": None,
            "region": None,
            "metadata": divMetadata_type(facet=[])
        }
        actual_div = self.actual_doc_2.binding.body.div[0].div[0]
        actual_divs_attr = Denester.merge_attr(parent_attr,Denester.div_attr(actual_div))
        assert excepted_div_attr["styles"] == actual_divs_attr["styles"]
    

    

    def test_recurse_many_child(self):
        expected_divs = self.expected_doc_2.binding.body.div
        nested_divs =  self.actual_doc_2.binding.body.div
        unnested_divs =  []
        for nested_div in nested_divs:
            unnested_divs.extend((Denester.combine_divs(Denester.recurse(nested_div))))
        assert len(unnested_divs) == len(expected_divs)

    def test_merged_attr_lang_only_on_child(self):
        expected_div_attr = {
            "styles" : ["S1","S2"],
            "lang" : "fr"
        }
        parent_attr = {
            "styles" : ["S2"],
            "lang": None,
            "region": None,
            "metadata": divMetadata_type(facet=[])
        }
        actual_div = self.actual_doc_2.binding.body.div[0].div[0]
        actual_divs_attr = Denester.merge_attr(parent_attr,Denester.div_attr(actual_div))
        assert expected_div_attr["lang"] == actual_divs_attr["lang"]
    
    def test_merged_attr_lang_only_on_parent(self):
        expected_div_attr = {
            "styles" : ["S1","S2"],
            "lang" : "fr"
        }
        parent_attr = {
            "styles" : ["S2"],
            "lang" : "fr",
            "region": None,
            "metadata": divMetadata_type(facet=[])
        }
        actual_div = self.actual_doc.binding.body.div[0].div[0]
        actual_divs_attr = Denester.merge_attr(parent_attr,Denester.div_attr(actual_div))
        assert expected_div_attr["lang"] == actual_divs_attr["lang"]

    def test_merged_attr_lang_only_on_both_child_and_parent(self):
        expected_div_attr = {
            "styles" : ["S1","S2"],
            "lang" : "en-GB"
        }
        parent_attr = {
            "styles" : ["S2"],
            "lang" : "fr",
            "region": None,
            "metadata": divMetadata_type(facet=[])
        }
        actual_div = self.actual_doc.binding.body.div[0].div[1]
        actual_divs_attr = Denester.merge_attr(parent_attr,Denester.div_attr(actual_div))
        assert expected_div_attr["lang"] == actual_divs_attr["lang"] 
    
    def test_merged_attr_different_region(self):
        expected_divs = self.expected_doc_3.binding.body.div
        nested_divs =  self.actual_doc_3.binding.body.div
        unnested_divs =  []
        for nested_div in nested_divs:
            unnested_divs.extend((Denester.combine_divs(Denester.recurse(nested_div))))
        assert len(expected_divs)== len(unnested_divs)

    def test_merged_attr_same_region(self):
        expected_divs = self.expected_doc_3.binding.body.div
        nested_divs =  self.actual_doc_3.binding.body.div
        unnested_divs =  []
        for nested_div in nested_divs:
            unnested_divs.extend((Denester.combine_divs(Denester.recurse(nested_div))))
        assert unnested_divs[0].region == expected_divs[0].region

    def test_combine_same_divs(self):
        expected_divs = self.expected_doc_2.binding.body.div
        nested_divs =  self.actual_doc_2.binding.body.div
        unnested_divs =  []
        for nested_div in nested_divs:
            unnested_divs.extend(Denester.combine_divs(Denester.recurse(nested_div)))
        assert len(unnested_divs) == len(expected_divs)
        
    def test_merged_metadata(self):
        expected_divs = self.expected_doc_2.binding.body.div
        nested_divs =  self.actual_doc_2.binding.body.div
        unnested_divs =  []
        for nested_div in nested_divs:
            unnested_divs.extend(Denester.combine_divs(Denester.recurse(nested_div)))
        assert len(unnested_divs) == len(expected_divs)
        i = 0
        print(unnested_divs)
        while i < len(unnested_divs):
            assert len(unnested_divs[i].metadata.facet) == len(expected_divs[i].metadata.facet)
            i += 1

