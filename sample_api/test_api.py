__version__ ='0.1'

import tornado.ioloop
import tornado.web
import argparse
import requests
from tornado import gen

class EndpointHandler(tornado.web.RequestHandler):

	@gen.coroutine
	def get(self):
		body="""<?xml version="1.0" encoding="UTF-8" ?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:exam="http://www.example.org">
                  <soapenv:Header/>
                  <soapenv:Body>
                    <exam:input>
                      <exam:request>test</exam:request>
                    </exam:input>
                 </soapenv:Body>
               </soapenv:Envelope>"""
		response = requests.post("http://localhost:8888/test",
                                 data=body, timeout=10)
		print("got first mock response")
		print(response.content)
		body="""<?xml version="1.0" encoding="UTF-8" ?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:exam="http://www.example.org">
                  <soapenv:Header/>
                  <soapenv:Body>
                    <exam:input>
                      <exam:request>test2</exam:request>
                    </exam:input>
                 </soapenv:Body>
               </soapenv:Envelope>"""
		response = requests.post("http://localhost:8888/test2",
                                 data=body, timeout=10)

		print("got second mock response")
		print(response.content)
		self.set_header("Content-type","application/xml")
		body = """<?xml version="1.0" encoding="UTF-8" ?>
		        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:exam="http://www.example.org">
                <soapenv:Header/>
                <soapenv:Body>
                  <exam:output>
                    <exam:result>SuccessGlobal!</exam:result>
                  </exam:output>
                </soapenv:Body>
              </soapenv:Envelope>"""
		self.write(body)


def register_app():
	return tornado.web.Application([
		(r"/.*", EndpointHandler)
	])

if __name__=="__main__":
	
	parser = argparse.ArgumentParser(prog='test_api.py',description="Simple orchestration service to use for demo")
	parser.add_argument('--port', '-p', help='Specify the listening port for your mock api', default=8888)
	parser.add_argument('--version', action='version', version='%(prog)s '+ __version__, help='Print the test_api version')
	args = parser.parse_args()
	
	app = register_app()
	app.listen(args.port)
	tornado.ioloop.IOLoop.current().start()