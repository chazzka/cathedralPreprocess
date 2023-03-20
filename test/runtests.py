import unittest

from preprocessing.preprocessing import getNumberEight
from preprocessing.preprocessing import CSVDateTimeToMilliseconds, apiDateTimeToMilliseconds
from service.request import fetchToJson, some
from mock.randomdatagenerator import combineListsOfStruct, Result


class TestPreprocessing(unittest.TestCase):

    def testSome(self):
        self.assertEqual(some(), 13)

    def testGetNumberEight(self):
        self.assertEqual(getNumberEight(), 8)

    def testDateTimeToMillisecondsCsv(self):
        self.assertEqual(CSVDateTimeToMilliseconds('2016-12-20 09:38:42.000'), 1482223122000.0)

    def testDateTimeToMillisecondsApi(self):
        self.assertEqual(apiDateTimeToMilliseconds('2016-12-20T09:38:42'), 1482223122000.0)


class TestRequest(unittest.TestCase):

    def testJSONFetch(self):
        self.assertEqual(fetchToJson('https://jsonplaceholder.typicode.com/users')[0]['username'], 'Bret')


class TestRandomGenerator(unittest.TestCase):
    
    def testCombineListOfStruct(self):
        self.assertEqual(combineListsOfStruct([Result([1,2,3],[4,5,6]), Result([1,2,3], [4,5,6])], 'x'), [1,2,3,1,2,3])

if __name__ == '__main__':
    unittest.main()