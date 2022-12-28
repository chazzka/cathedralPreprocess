import unittest

from src.preprocessing.preprocessing import getNumberEight
from src.preprocessing.preprocessing import CSVDateTimeToMilliseconds, apiDateTimeToMilliseconds
from src.service.request import fetchToJson

class TestPreprocessing(unittest.TestCase):

    def testGetNumberEight(self):
        self.assertEqual(getNumberEight(), 8)

    def testDateTimeToMillisecondsCsv(self):
        self.assertEqual(CSVDateTimeToMilliseconds('2016-12-20 09:38:42.000'), 1482223122000.0)

    def testDateTimeToMillisecondsApi(self):
        self.assertEqual(apiDateTimeToMilliseconds('2016-12-20T09:38:42'), 1482223122000.0)


class TestRequest(unittest.TestCase):

    def testJSONFetch(self):
        self.assertEqual(fetchToJson('https://jsonplaceholder.typicode.com/users')[0]['username'], 'Bret')

    

if __name__ == '__main__':
    unittest.main()