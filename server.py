#!/usr/bin/python
import requests
from pathparser import PathParser
from bs4 import BeautifulSoup
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		
		print self.path
		if self.path != '/':
			path = PathParser(self.path)
			if path.components[0] == 'api':
				msg = 'snow'
				print "fetching"
				path = PathParser(self.path)
				print path.components
				if path.components[1] == 'snow-forecast.com':
					msg = snowdata(self.path[5:])
					print msg
			
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				# Send the html message
				# message = snowdata()
				self.wfile.write(msg)
				return	
		else:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			# Send the html message
			self.wfile.write("Hello World !")
			return

		
		

def snowdata(urlend):
	print urlend
	r = requests.get('https://www.' + urlend)
	soup = BeautifulSoup(r.text, 'html.parser')
	d = {}
	d["oneday"] = 0
	d["threeday"] = 0
	d["sixday"] = 0
	d["onedayr"] = 0
	d["threedayr"] = 0
	d["sixdayr"] = 0
	snowlist = soup.find_all("td", class_ =  ["snowy", "snowy day-end"])
	rainlist = soup.find_all("td", class_ =  ["rainy", "rainy day-end"])
	for count in range(0,len(snowlist)):
		if rainlist[count].text == '-':
			continue
		if count < 3:
			d["onedayr"] += int(rainlist[count].text)
		if count < 9:
			d["threedayr"] += int(rainlist[count].text)
		
		d["sixdayr"] += int(rainlist[count].text)
	for count in range(0,len(snowlist)):
		if snowlist[count].text == "-":
			continue
		if count < 3:
			d["oneday"] += int(snowlist[count].text)
		if count < 9:
			d["threeday"] += int(snowlist[count].text)
		
		d["sixday"] += int(snowlist[count].text)
	
	return json.dumps(d)


snowdict = json.loads(snowdata('snow-forecast.com/resorts/Turoa/6day/top'))

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	print 'hello'
	print snowdict
	print "One Day Forecast: " + str(snowdict["oneday"])
	print "Three Day Forecast: " + str(snowdict['threeday'])
	print "Six Day Forecast: " + str(snowdict['sixday'])

	
	
	#Wait forever for incoming htto requests

	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()