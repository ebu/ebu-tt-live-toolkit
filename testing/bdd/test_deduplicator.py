from ebu_tt_live.node.deduplicator import DeDuplicatorNode
from ebu_tt_live.node.base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3Document
from ebu_tt_live.bindings import style_type, region_type
from ebu_tt_live.carriage.interface import IProducerCarriage, IConsumerCarriage
from mock import MagicMock
from pytest_bdd import scenarios, when, then, given
import six

scenarios('features/deduplicator/deduplicator-blackbox.feature')


@given('a deduplicator node')
def given_deduplicator_node(template_dict):
    template_dict.clear()
    instance = DeDuplicatorNode(
        node_id='testDeDuplicatorNode',
        sequence_identifier='testDeDuplicated1'
    )
    return instance


@when('the document is processed')
def when_document_processed(given_deduplicator_node, xml_file):
    given_deduplicator_node.process_document(document=xml_file)
    given_deduplicator_node.producer_carriage.emit_data(data=document, **kwargs)
#    given_deduplicator_node.producer_carriage.reset_mock()


@then('the output document has <style_out_num> styles')
def then_document_has_styles(template_dict, style_out_num, new_style_list):
    template_dict['style_out_num'] = style_out_num
    new_style_list = xml_file.new_style_list
    assert style_out_num == len(new_style_list)



@then('it has <region_out_num> regions')
def then_document_has_regions(template_dict, region_out_num, new_region_list):
    template_dict['region_out_num'] = region_out_num
    new_region_list = xml_file.new_region_list
    assert region_out_num == len(new_region_list)



# @then('the <xml_id> is replaced by <new_label>')
# def then_replace_id(template_dict, xml_id, new_label):
#     template_dict.clear()
#     new_dummy_doc = sequence.new_document()
#     template_dict['xml_id'] = new_dummy_doc.xml_id
#     template_dict['new_label'] = new_dummy_doc.new_label
#
#
# @when('it has style attributes <style_1>')
# def when_style_attribute_one(template_dict, style_1):
#     template_dict.clear()
#     new_dummy_doc = sequence.new_document()
#     template_dict['style_1'] = new_dummy_doc.style_1
#
#
# @when('it has style attributes <style_2')
# def when_style_attribute_two(template_dict, style_2):
#     template_dict['style_2'] = new_dummy_doc.style_2
#
#
# @then('<id_1> and <id_2> are replaced with the same <new_label>')
# def then_style_attributes_same(template_file, template_dict, sequence, id_1, id_2, new_label):
#     template_dict['id_1'] = new_dummy_doc.id_1
#     template_dict['id_2'] = new_dummy_doc.id_2
#     template_dict['new_label'] = new_dummy_doc.new_label
#     xml_file = template_file.render(template_dict)
#     document = EBUTT3Document.create_from_xml(xml_file)
#     sequence.add_document(document)
#
#
# @then('<id_1> is replaced with <new_label_1>')
# def then_replace_id_one_with_new_label_one(template_dict, id_1, new_label_1):
#     template_dict['id_1'] = new_dummy_doc.id_1
#     template_dict['new_label_1'] = new_dummy_doc.new_label_1
#
#
# @then('<id_2> is replaced with <new_label_2>')
# def then_replace_id_two_with_new_label_two(template_dict, id_2, new_label_2):
#     template_dict['id_2'] = new_dummy_doc.id_2
#     template_dict['new_label_2'] = new_dummy_doc.new_label_2
#
#
# @when('it has element name <element_name>')
# def when_element_name(template_dict, element_name):
#     template_dict['element_name'] = new_dummy_doc.element_name
#
#
# @when('it has old id <old_id>')
# def when_stored_name(template_dict, old_id):
#     template_dict['old_id'] = new_dummy_doc.old_id
#
#
# @then('replace with <new_label>')
# def then_replace_element_name_and_old_id(template_dict, new_label):
#     template_dict['new_label'] = new_dummy_doc.new_label
#
#
# @when('it has reference <old_style_reference>')
# def when_it_has_old_reference(template_dict, old_style_reference):
#     template_dict['old_style_reference'] = new_dummy_doc.old_style_reference
#
#
# @then('replace with <new_style_reference>')
# def then_replace_with_new_reference(template_dict, new_style_reference):
#     template_dict['new_style_reference'] = new_dummy_doc.new_style_reference
