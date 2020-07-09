from unittest import TestCase
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import roundAndStrip


class testRoundAndStrip(TestCase):

    def testRoundUp(self):
        self.assertEqual(
            roundAndStrip(123.45, 1),
            '123.5'
        )
        self.assertEqual(
            roundAndStrip(123.456, 2),
            '123.46'
        )

    def testRoundDown(self):
        self.assertEqual(
            roundAndStrip(123.44, 1),
            '123.4'
        )
        self.assertEqual(
            roundAndStrip(123.554, 2),
            '123.55'
        )

    def testStripTrailingZeros(self):
        self.assertEqual(
            roundAndStrip(123.100, 3),
            '123.1'
        )
        self.assertEqual(
            roundAndStrip(123.000, 2),
            '123'
        )


    def testStripTrailingDecimalPoint(self):
        self.assertEqual(
            roundAndStrip(122.999, 2),
            '123'
        )

    def testDontStripSignificantZeros(self):
        self.assertEqual(
            roundAndStrip(100, 0),
            '100'
        )

    def testNegativeDecimalPlaces(self):
        self.assertEqual(
            roundAndStrip(123, -1),
            '120'
        )
