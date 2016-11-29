from unittest import TestCase
from ebu_tt_live.carriage import base as carriage_base


class TestABCs(TestCase):

    def test_interfaces(self):
        self.assertRaises(TypeError, carriage_base.ICarriageMechanism)
        self.assertRaises(TypeError, carriage_base.IProducerCarriage)
        self.assertRaises(TypeError, carriage_base.IConsumerCarriage)

    def test_abstract_classes(self):
        self.assertRaises(TypeError, carriage_base.AbstractProducerCarriage)
        self.assertRaises(TypeError, carriage_base.AbstractConsumerCarriage)
        self.assertRaises(TypeError, carriage_base.AbstractCombinedCarriage)
