import unittest

from src.preprocessing.preprocessing import getNumberEight

class TestPreprocessing(unittest.TestCase):

    def testGetNumberEight(self):
        self.assertEqual(getNumberEight(), 8)

if __name__ == '__main__':
    unittest.main()