__version__ ='0.1'

import argparse
import unittest
import sys

import re
import yaml
import os

import tornado.web
from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient
from mock_handler import MockHandler


def flatten_text(text):
    return re.sub(r"\s+", " ", text)


def genTestFunc():
    def test_api(self):
        self.mock_requests = {}
        # invoke service to be tested
        client = AsyncHTTPClient(self.io_loop)

        client.fetch(self.test_data['service_endpoint'], self.stop)
        response = self.wait()

        mocks_with_assertions = [x for x in self.test_data['mocks'] if 'body' in x['mock']['request']]
        for mock in mocks_with_assertions:
            self.wait(timeout=30)
            self.assertEqual(flatten_text(self.mock_requests[mock['mock']['name']].decode("utf-8")), flatten_text(mock['mock']['request']['body']))
            #TODO: Assert request headers

        print(response)

        # perform assertions
        for assertion in self.test_data['assertions']:
            if 'http_code' in assertion:
                self.assertEqual(response.code, assertion['http_code'])
            if 'response' in assertion:
                self.assertEqual(flatten_text(response.body.decode("utf-8")), flatten_text(assertion['response']))
            if 'content-type' in assertion:
                self.assertEqual(response.headers['Content-Type'], assertion['content-type'])
    return test_api

def genSetup(filename):

    def setUp(self):
        super(BaseClass,self).setUp()
        with open(filename) as data_file:
            self.test_data = yaml.load(data_file)
        print(filename)
    return setUp
            
 
class BaseClass(AsyncHTTPTestCase):

    def get_app(self):
        #Create a generic route handler
        application = tornado.web.Application([
        (r"/.*", MockHandler, {"test":self}), ])
        application.listen(port)

        return application


def get_yaml_files(path):
    files = os.listdir(path)
    return filter(lambda file: re.match(".*\.yaml$", file), files)


def generate_tst_classes(folder):
    tests = get_yaml_files(folder)
    for test in tests:
        testName = "test_" + test.split(".")[0]
        globals()[testName] = type(testName,(BaseClass,),{"setUp":genSetup(folder + "/" + test), testName: genTestFunc()})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='api_tester.py',description="API Tester allows you to test API's using a configuration file to specify tests")
    parser.add_argument('--port', '-p', help='Specify the listening port for your mock server', default=8888)
    parser.add_argument('--folder', '-f', help='Specify the folder that will be containing the test case definitions', required=True)
    parser.add_argument('--version', action='version', version='%(prog)s '+ __version__, help='Print the API Tester version')
    args = parser.parse_args()
    port = args.port

    del(sys.argv[1:])
    generate_tst_classes(args.folder)
    unittest.main()

else:
    folder = os.environ.get("test_folder", "sample_tests")
    port = os.environ.get("test_port", "8888")
    generate_tst_classes(folder)




