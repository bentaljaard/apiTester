from tornado.web import RequestHandler

class MockHandler(RequestHandler):
    def initialize(self, test):
        self.test = test
        self.test_data = test.test_data

    def get(self):
        # get list of mocks with GET operation
        mocks = [x for x in self.test_data['mocks'] if x['mock']['request']['method'] == "GET"]

        #Check if we are mocking a service with this uri
        #TODO: Add support for regex uri
        if self.request.uri not in [mock['mock']['request']['url'] for mock in mocks]:
                raise tornado.web.HTTPError(404)
        else:
            for mock in mocks:
                if self.request.uri == mock['mock']['request']['url']:
                    #set http response code
                    self.set_status(mock['mock']['response']['status'])

                    #assign headers for response
                    headers = mock['mock']['response']['headers']
                    for headerName, headerValue in headers.items():
                        self.set_header(headerName, headerValue)

                    #return mock response
                    self.write(mock['mock']['response']['body'])

                #TODO: Assertions for GET requests
        

    def post(self):
         # get list of mocks with POST operation
        mocks = [x for x in self.test_data['mocks'] if x['mock']['request']['method'] == "POST"]

        #Check if we are mocking a service with this uri
        if self.request.uri not in [mock['mock']['request']['url'] for mock in mocks]:
                raise tornado.web.HTTPError(404)
        else:
            for mock in mocks:
                if self.request.uri == mock['mock']['request']['url']:
                    #set http response code
                    self.set_status(mock['mock']['response']['status'])

                    #assign headers for response
                    headers = mock['mock']['response']['headers']
                    for headerName, headerValue in headers.items():
                        self.set_header(headerName, headerValue)

                    #return mock response
                    self.write(mock['mock']['response']['body'])

                #save request for assertions
                if mock['mock']['request']['body']:
                    self.test.mock_requests[mock['mock']['name']] = self.request.body
                    self.test.stop()
