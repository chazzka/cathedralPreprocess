import unittest

from preprocessing.preprocessing import getNumberEight, preprocessAPIDict, mapcol, CSVDateTimeToMilliseconds, apiDateTimeToMilliseconds, replaceNoKeyWithValue
from service.request import fetchToJson, some
from mock.randomdatagenerator import combineListsOfStruct, Result


class TestPreprocessing(unittest.TestCase):

    def testSome(self):
        self.assertEqual(some(), 13)

    def testGetNumberEight(self):
        self.assertEqual(getNumberEight(), 8)

    def testDateTimeToMillisecondsCsv(self):
        self.assertEqual(CSVDateTimeToMilliseconds(
            '2016-12-20 09:38:42.000'), 1482223122000.0)

    def testDateTimeToMillisecondsApi(self):
        self.assertEqual(apiDateTimeToMilliseconds(
            '2016-12-20T09:38:42'), 1482223122000.0)

    def testMapCol(self):
        s = [{'name': 'Adam', 'age': 16}, {'name': 'Oto', 'age': 26}]

        res = mapcol('age', lambda x: x+1)(s[0])
        self.assertEqual(res['age'], 17)


    def testReplaceNoKeyWithValue(self):
        s = {"name": "Adam"}
        res = {"name": "Adam", "age": 15.5}

        self.assertEqual(s, {"name": "Adam"})
        self.assertEqual(replaceNoKeyWithValue(s, "age", 15.5), res)

    def testPreprocessAPIDict(self):
        # TODO: mrkni jak to chodi z bakcnedu a napiš test aby se ty prázdné hodnoty tady přehodily na 0, None to asi nebude
        s = [{'time': '2016-12-20T09:38:42'}, {'time': '2016-12-20T09:38:42', 'average': '45'}]
        res = [{'time': 1482223122000.0, 'average': 0.0}, {'time': 1482223122000.0, 'average': 45.0}]

        cal = preprocessAPIDict(s, {"timeColumnName": 'time', "averageColumnName":'average'})
        
        self.assertEqual(res, cal)


class TestRequest(unittest.TestCase):

    def testJSONFetch(self):
        self.assertEqual(fetchToJson(
            'https://jsonplaceholder.typicode.com/users')[0]['username'], 'Bret')


class TestRandomGenerator(unittest.TestCase):

    def testCombineListOfStruct(self):
        self.assertEqual(combineListsOfStruct([Result([1, 2, 3], [4, 5, 6]), Result(
            [1, 2, 3], [4, 5, 6])], 'x'), [1, 2, 3, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
