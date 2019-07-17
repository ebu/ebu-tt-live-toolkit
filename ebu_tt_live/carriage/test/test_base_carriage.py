from unittest import TestCase
from ebu_tt_live.carriage import interface as carriage_interface
from ebu_tt_live.carriage import base as carriage_base
from ebu_tt_live.node import interface as node_interface
from ebu_tt_live.errors import ComponentCompatError, DataCompatError
from mock import MagicMock


class DummyDataTypeA(object):
    pass


class DummyDataTypeB(object):
    pass


class TestABCs(TestCase):

    def test_interfaces(self):
        self.assertRaises(TypeError, carriage_interface.ICarriageMechanism)
        self.assertRaises(TypeError, carriage_interface.IProducerCarriage)
        self.assertRaises(TypeError, carriage_interface.IConsumerCarriage)

    def test_abstract_classes(self):
        self.assertRaises(TypeError, carriage_base.AbstractProducerCarriage)
        self.assertRaises(TypeError, carriage_base.AbstractConsumerCarriage)
        self.assertRaises(TypeError, carriage_base.AbstractCombinedCarriage)


class TestDummyCarriages(TestCase):

    def setUp(self):
        prod_node = MagicMock(spec=node_interface.IProducerNode)
        prod_node.provides.return_value = DummyDataTypeA
        self._producer_node = prod_node

        cons_node = MagicMock(spec=node_interface.IConsumerNode)
        cons_node.expects.return_value = DummyDataTypeA
        self._consumer_node = cons_node

        # We can't unittest with combined mocked out because MagicMock can't emulate 2 interfaces
        # comb_node = MagicMock(spec=[node_interface.IProducerNode, node_interface.IConsumerNode])
        # comb_node.provides.return_value = DummyDataTypeA
        # comb_node.expects.return_value = DummyDataTypeA
        # self._combined_node = comb_node

    def _get_dummy_producer_carriage(self, expects):
        class DummyProducerCarriage(carriage_base.AbstractProducerCarriage):

            _expects = expects

            def emit_data(self, data, **kwargs):
                pass

        return DummyProducerCarriage()

    def _get_dummy_consumer_carriage(self, provides):
        class DummyConsumerCarriage(carriage_base.AbstractConsumerCarriage):

            _provides = provides

            def on_new_data(self, data, **kwargs):
                pass

        return DummyConsumerCarriage()

    def _get_dummy_combined_carriage(self, expects, provides):
        class DummyCombinedCarriage(carriage_base.AbstractCombinedCarriage):

            _expects = expects
            _provides = provides

            def emit_data(self, data, **kwargs):
                pass

            def on_new_data(self, data, **kwargs):
                pass

        return DummyCombinedCarriage()

    def test_dummy_producer_success(self):
        producer_carriage = self._get_dummy_producer_carriage(DummyDataTypeA)
        producer_carriage.register_producer_node(self._producer_node)
        self.assertEqual(producer_carriage.producer_node, self._producer_node)

    def test_dummy_producer_incompatible_interface(self):
        producer_carriage = self._get_dummy_producer_carriage(DummyDataTypeA)
        self.assertRaises(ComponentCompatError, producer_carriage.register_producer_node, self._consumer_node)
        self.assertIsNone(producer_carriage.producer_node)

    def test_dummy_producer_incompatible_data(self):
        producer_carriage = self._get_dummy_producer_carriage(DummyDataTypeB)
        self.assertRaises(DataCompatError, producer_carriage.register_producer_node, self._producer_node)
        self.assertIsNone(producer_carriage.producer_node)
        
    def test_dummy_consumer_success(self):
        consumer_carriage = self._get_dummy_consumer_carriage(DummyDataTypeA)
        consumer_carriage.register_consumer_node(self._consumer_node)
        self.assertEqual(consumer_carriage.consumer_node, self._consumer_node)

    def test_dummy_consumer_incompatible_interface(self):
        consumer_carriage = self._get_dummy_consumer_carriage(DummyDataTypeA)
        self.assertRaises(ComponentCompatError, consumer_carriage.register_consumer_node, self._producer_node)
        self.assertIsNone(consumer_carriage.consumer_node)

    def test_dummy_consumer_incompatible_data(self):
        consumer_carriage = self._get_dummy_consumer_carriage(DummyDataTypeB)
        self.assertRaises(DataCompatError, consumer_carriage.register_consumer_node, self._consumer_node)
        self.assertIsNone(consumer_carriage.consumer_node)
        
    def test_dummy_combined_success_with_producer(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeA, provides=DummyDataTypeA)
        combined_carriage.register_producer_node(self._producer_node)
        self.assertEqual(combined_carriage.producer_node, self._producer_node)

    def test_dummy_combined_success_with_consumer(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeA, provides=DummyDataTypeA)
        combined_carriage.register_consumer_node(self._consumer_node)
        self.assertEqual(combined_carriage.consumer_node, self._consumer_node)

    def test_dummy_combined_success_with_both(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeA, provides=DummyDataTypeA)
        combined_carriage.register_producer_node(self._producer_node)
        combined_carriage.register_consumer_node(self._consumer_node)
        self.assertEqual(combined_carriage.producer_node, self._producer_node)
        self.assertEqual(combined_carriage.consumer_node, self._consumer_node)

    def test_dummy_combined_incompatible_interface_with_consumer(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeA, provides=DummyDataTypeA)
        self.assertRaises(ComponentCompatError, combined_carriage.register_consumer_node, self._producer_node)
        self.assertIsNone(combined_carriage.consumer_node)

    def test_dummy_combined_incompatible_interface_with_producer(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeA, provides=DummyDataTypeA)
        self.assertRaises(ComponentCompatError, combined_carriage.register_producer_node, self._consumer_node)
        self.assertIsNone(combined_carriage.producer_node)

    def test_dummy_combined_incompatible_data_with_consumer(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeA, provides=DummyDataTypeB)
        self.assertRaises(DataCompatError, combined_carriage.register_consumer_node, self._consumer_node)
        self.assertIsNone(combined_carriage.consumer_node)

    def test_dummy_combined_incompatible_data_with_producer(self):
        combined_carriage = self._get_dummy_combined_carriage(expects=DummyDataTypeB, provides=DummyDataTypeA)
        self.assertRaises(DataCompatError, combined_carriage.register_producer_node, self._producer_node)
        self.assertIsNone(combined_carriage.producer_node)
