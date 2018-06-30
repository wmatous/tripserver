#!/usr/bin/python
import requests
from pathparser import PathParser
from bs4 import BeautifulSoup
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		
		print self.path
		if self.path != '/':
			msg = 'snow'
			path = PathParser(self.path)
			print path.components
			if path.components[0] == 'forecast':
				msg = snowdata(''.join(path.components[1:]))
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
	r = requests.get('https://www.snow-forecast.com/resorts/' + urlend)
	soup = BeautifulSoup(r.text, 'html.parser')
	d = {}
	d['oneday'] = 0
	d['threeday'] = 0
	d['sixday'] = 0
	snowlist = soup.find_all("td", class_ =  ["snowy", "snowy day-end"])
	for count in range(0,len(snowlist)):
		if snowlist[count].text == '-':
			continue
		if count < 3:
			d['oneday'] += int(snowlist[count].text)
		if count < 9:
			d['threeday'] += int(snowlist[count].text)
		
		d['sixday'] += int(snowlist[count].text)
	
	return d


snowdict = snowdata('https://www.snow-forecast.com/resorts/Turoa/6day/top')

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	print "One Day Forecast: " + str(snowdict['oneday'])
	print "Three Day Forecast: " + str(snowdict['threeday'])
	print "Six Day Forecast: " + str(snowdict['sixday'])

	
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()