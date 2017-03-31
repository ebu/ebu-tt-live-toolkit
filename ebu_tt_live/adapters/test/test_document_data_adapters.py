import os
import six
import weakref
import gc
from unittest import TestCase
from ebu_tt_live import documents
from ebu_tt_live.adapters.base import IDocumentDataAdapter
from ebu_tt_live.adapters import document_data
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError


class DummyDataTypeA(object):
    pass


class DummyDataTypeB(object):
    pass


class TestIDocumentDataAdapter(TestCase):

    def test_create(self):
        self.assertRaises(TypeError, IDocumentDataAdapter)

    def _get_simple_adapter(self):
        class SimpleTestAdapter(IDocumentDataAdapter):
            _expects = DummyDataTypeA
            _provides = DummyDataTypeB

            def convert_data(inner, data, **kwargs):
                return data, kwargs

        return SimpleTestAdapter

    def test_simple_subclass(self):
        impl_class = self._get_simple_adapter()

        wref = weakref.ref(impl_class)

        self.assertIsInstance(
            document_data.get_document_data_adapter(DummyDataTypeA, DummyDataTypeB),
            impl_class
        )
        gc.collect()
        # It should not be garbage collected
        self.assertIsInstance(
            document_data.get_document_data_adapter(DummyDataTypeA, DummyDataTypeB),
            impl_class
        )

        del impl_class
        gc.collect()
        # When the class goes out of scope it is supposed to be removed from the mapping.
        self.assertIsNone(wref())
        self.assertRaises(ValueError, document_data.get_document_data_adapter, DummyDataTypeA, DummyDataTypeB)

        # Let's add it in again
        impl_class = self._get_simple_adapter()
        wref = weakref.ref(impl_class)

        # Check if it got back in the mapping
        self.assertIsInstance(
            document_data.get_document_data_adapter(DummyDataTypeA, DummyDataTypeB),
            impl_class
        )

        del impl_class
        gc.collect()
        # Verify full cleanup again
        self.assertIsNone(wref())
        self.assertRaises(ValueError, document_data.get_document_data_adapter, DummyDataTypeA, DummyDataTypeB)


class TestXMLtoEBUTT3Adapter(TestCase):

    _adapter_class = document_data.XMLtoEBUTT3Adapter
    _test_xml_file = 'testSeq_1.xml'
    _test_data_dir_path = os.path.join(os.path.dirname(__file__), 'test_data')
    _test_xml_path = os.path.join(_test_data_dir_path, _test_xml_file)
    _output_type = documents.EBUTT3Document
    _expected_keys = [
        'raw_xml'
    ]
    instance = None

    def setUp(self):
        self.instance = self._adapter_class()
        self.assertIsInstance(self.instance, IDocumentDataAdapter)

    def _assert_output_type(self, result):
        self.assertIsInstance(result, self._output_type)

    def _assert_kwargs_passtrough(self, result_kwargs, expected_keys):
        self.assertEquals(set(result_kwargs.keys()), set(expected_keys))

    def _get_xml(self):
        with open(self._test_xml_path, 'r') as xml_file:
            xml_data = xml_file.read()
        return xml_data

    def _get_input(self):
        return self._get_xml()

    def test_success(self):
        expected_keys = []
        expected_keys.extend(self._expected_keys)
        result, res_kwargs = self.instance.convert_data(self._get_input())
        self._assert_output_type(result)
        self._assert_kwargs_passtrough(res_kwargs, expected_keys)

    def test_kwargs_passthrough(self):
        in_kwargs = {
            'foo': 'bar'
        }
        expected_keys = ['foo']
        expected_keys.extend(self._expected_keys)
        result, res_kwargs = self.instance.convert_data(self._get_input(), **in_kwargs)
        self._assert_kwargs_passtrough(res_kwargs, expected_keys)

    def test_sequence_id_match(self):
        result, res_kwargs = self.instance.convert_data(
            self._get_input(),
            sequence_identifier='TestSequence1'
        )

    def test_sequence_id_mismatch(self):
        # This test emulates a document being parsed and the sequenceIdentifier not matching the
        # expected one in the kwargs. This (in the websocket case) should cause the connection to
        # be broken.

        with self.assertRaises(UnexpectedSequenceIdentifierError) as exc:
            self.instance.convert_data(
                self._get_input(),
                sequence_identifier='wrong'
            )


class TestXMLtoEBUTTDAdapter(TestCase):
    _output_type = documents.EBUTTDDocument
    _adapter_class = document_data.XMLtoEBUTTDAdapter
    _expected_keys = []

    # TODO: Finish this once we have EBUTT-D parsing


class TestEBUTT3toXMLAdapter(TestXMLtoEBUTT3Adapter):
    _output_type = six.text_type
    _adapter_class = document_data.EBUTT3toXMLAdapter
    _expected_keys = [
        'sequence_identifier',
        'sequence_number',
        'availability_time',
        'time_base',
        'clock_mode'
    ]

    def _get_input(self):
        return documents.EBUTT3Document.create_from_xml(self._get_xml())

    def test_sequence_id_mismatch(self):
        pass

    def test_sequence_id_match(self):
        pass


class TestEBUTTDtoXMLAdapter(TestEBUTT3toXMLAdapter):
    _adapter_class = document_data.EBUTTDtoXMLAdapter
    _expected_keys = []

    def _get_input(self):
        input_doc = documents.EBUTTDDocument(lang='en-GB')
        return input_doc

    def test_sequence_id_mismatch(self):
        pass

    def test_sequence_id_match(self):
        pass


class TestEBUTT3toEBUTTDAdapter(TestXMLtoEBUTT3Adapter):
    _adapter_class = document_data.EBUTT3toEBUTTDAdapter
    _output_type = documents.EBUTTDDocument
    _expected_keys = []

    def _get_input(self):
        return documents.EBUTT3Document.create_from_xml(self._get_xml())

    def test_sequence_id_mismatch(self):
        pass

    def test_sequence_id_match(self):
        pass
