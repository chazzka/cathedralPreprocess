import unittest

from src.preprocessing.preprocessing import getNumberEight
from src.preprocessing.preprocessing import CSVDateTimeToMilliseconds
from src.service.request import fetchToJson
from src.service.request import jsonDestringify

class TestPreprocessing(unittest.TestCase):

    def testGetNumberEight(self):
        self.assertEqual(getNumberEight(), 8)

    def testDateTimeToMilliseconds(self):
        self.assertEqual(CSVDateTimeToMilliseconds('2016-12-20 09:38:42.000'), 1482223122000.0)


class TestRequest(unittest.TestCase):

    def testJSONFetch(self):
        self.assertEqual(fetchToJson('https://jsonplaceholder.typicode.com/users')[0]['username'], 'Bret')

    def testJsonDestringify(self):
        test = "<FIELD attrname=\"dDevdCasZpravy\" caption=\"Čas zprávy\" visible=\"TRUE\" orderby=\"0\" readonly=\"0\" fieldtype=\"dateTime\"/>\r\n"
        res = jsonDestringify(test)
        self.assertEqual(res, '<FIELD attrname="dDevdCasZpravy" caption="Čas zprávy" visible="TRUE" orderby="0" readonly="0" fieldtype="dateTime"/>')
    
    

if __name__ == '__main__':
    unittest.main()