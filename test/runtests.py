import unittest

from src.preprocessing.preprocessing import getNumberEight
from src.preprocessing.preprocessing import dateTimeToMilliseconds

class TestPreprocessing(unittest.TestCase):

    def testGetNumberEight(self):
        self.assertEqual(getNumberEight(), 8)

    def testDateTimeToMilliseconds(self):
        self.assertEqual(dateTimeToMilliseconds('2016-12-20 09:38:42.000'), 1482223122000.0)

if __name__ == '__main__':
    unittest.main()