#!/usr/bin/python

import time
from picamera import PiCamera

import BaseHTTPServer

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
#camera.start_preview()

#camera warm-up time
time.sleep(2)

# hosting
HOST_NAME = "pi-noir-camera.local"
PORT_NUMBER = 8000 # Magic number. Can't bind under 1024 on normal user accounts; port 80 is the normal HTTP port
WEBCAM_FILENAME = "webcam.jpg"

class SimpleCloudFileServer(BaseHTTPServer.BaseHTTPRequestHandler):
	def sendHeader(self, response=200, contentType="image/jpeg"):
		self.send_response(response)
		self.send_header("Content-type", contentType)
		self.end_headers()
	
	def contentTypeFrom(self, filename):
		if filename.endswith("html"):
			return "text/html"
		elif filename.endswith("css"):
			return "text/css"
		elif filename.endswith("jpg") or fiename.endswith("jpeg"):
			return "image/jpeg"
		elif filename.endswith("png"):
			return "image/png"
		elif filename.endswith("svg"):
			return "image/svg+xml"
	
	def do_HEAD(self):
		self.sendHeader()
	
	def do_GET(self):
		filename = (self.path[1:]).split("?")[0]
		
		if (filename==WEBCAM_FILENAME):
			camera.capture(WEBCAM_FILENAME)
		try:
			with open(filename, "rb") as in_file:
				data = in_file.read()
				self.sendHeader(contentType=self.contentTypeFrom(filename))
				self.wfile.write(data)
		except:
			printServerMessage("File not found: " + filename)
			self.sendHeader(response=404, contentType="text/plain")
			self.wfile.write("404 file not found")

def printServerMessage(customMessage):
	print customMessage, "(Time: %s, Host: %s, port: %s)" % (time.asctime(), HOST_NAME, PORT_NUMBER)
	
if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), SimpleCloudFileServer)
	
	printServerMessage("Server startup")
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	printServerMessage("Server stop")
