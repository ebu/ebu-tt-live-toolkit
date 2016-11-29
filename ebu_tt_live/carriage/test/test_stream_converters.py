# import os
# import unittest
# from ebu_tt_live.node import Node
# from ebu_tt_live.carriage import stream_converters
# from ebu_tt_live.carriage.base import CombinedCarriageImpl
# from ebu_tt_live import documents
# from mock import MagicMock
#
#
# class TestXMLEBUTT3DocumentStream(unittest.TestCase):
#
#     _converter_class = stream_converters.XMLtoEBUTT3DocumentStream
#     _document_class = documents.EBUTT3Document
#     _test_xml_file = 'testSeq_1.xml'
#     _test_data_dir_path = os.path.join(os.path.dirname(__file__), 'test_data')
#     _test_xml_path = os.path.join(_test_data_dir_path, _test_xml_file)
#
#     def _get_document(self):
#         return self._document_class.create_from_xml(
#             self.xml_document
#         )
#
#     def _get_processing_node(self):
#         return MagicMock()
#
#     def _get_next_carriage(self):
#         return MagicMock()
#
#     def _get_converter_instance(self):
#         instance = self._converter_class(carriage_impl=self.carriage)
#         instance.register(self.processing_node)
#         return instance
#
#     def _get_xml_document(self):
#         with open(self._test_xml_path, 'r') as xml_file:
#             xml_data = xml_file.read()
#         return xml_data
#
#     def setUp(self):
#         self.xml_document = self._get_xml_document()
#         self.document = self._get_document()
#         self.carriage = self._get_next_carriage()
#         self.processing_node = self._get_processing_node()
#         self.converter = self._get_converter_instance()
#
#     def _assert_sent_to_carriage(self, obj_type):
#         # This is the emit_data and process_document
#         self.carriage.emit_data.assert_called_once()
#         call_args, call_kwargs = self.carriage.emit_data.call_args
#         self.assertTrue(any(
#             map(lambda x: isinstance(x, obj_type), call_args) or \
#             map(lambda x: isinstance(x, obj_type), call_kwargs.values())
#         ))
#
#     def _assert_sent_to_node(self, obj_type):
#         # This is on_new_data
#         self.processing_node.process_document.assert_called_once()
#         call_args, call_kwargs = self.processing_node.process_document.call_args
#         self.assertTrue(any(
#             map(lambda x: isinstance(x, obj_type), call_args) or \
#             map(lambda x: isinstance(x, obj_type), call_kwargs.values())
#         ))
#
#     def test_creation(self):
#         self.carriage.register.assert_called_with(self.converter)
#         self.assertEquals(self.converter.node, self.processing_node)
#         self.assertEquals(self.converter._carriage_impl, self.carriage)
#
#     def test_process_document(self):
#         self.converter.process_document(self.xml_document)
#         self._assert_sent_to_node(self._document_class)
#
#     def test_emit_data(self):
#         self.converter.emit_data(self.xml_document)
#         self._assert_sent_to_carriage(self._document_class)
#
#     def test_on_new_data(self):
#         self.converter.on_new_data(self.xml_document)
#         self._assert_sent_to_node(self._document_class)
#
#
# class TestEBUTT3DocumenttoXMLStream(TestXMLEBUTT3DocumentStream):
#
#     _converter_class = stream_converters.EBUTT3DocumenttoXMLStream
#
#     def test_emit_data(self):
#         self.converter.emit_data(self.document)
#         self._assert_sent_to_carriage(basestring)
#
#     def test_on_new_data(self):
#         self.converter.on_new_data(self.document)
#         self._assert_sent_to_node(basestring)
#
#     def test_process_document(self):
#         self.converter.process_document(self.document)
#         self._assert_sent_to_node(basestring)
#
#
# class TestEBUTT3DocumenttoEBUTTDDocumentStream(TestXMLEBUTT3DocumentStream):
#
#     _converter_class = stream_converters.EBUTT3toEBUTTDStream
#     _target_data_type = documents.EBUTTDDocument
#
#     def test_emit_data(self):
#         self.converter.emit_data(self.document)
#         self._assert_sent_to_carriage(self._target_data_type)
#
#     def test_on_new_data(self):
#         self.converter.on_new_data(self.document)
#         self._assert_sent_to_node(self._target_data_type)
#
#     def test_process_document(self):
#         self.converter.process_document(self.document)
#         self._assert_sent_to_node(self._target_data_type)
