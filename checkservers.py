#!/usr/bin/env python
# Copyright (c) 2009, Steve Oliver (steve@xercestech.com)
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY STEVE OLIVER ''AS IS'' AND ANY
#EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL STEVE OLIVER BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api.urlfetch import DownloadError

import cgi
import datetime
import time
import logging
import wsgiref.handlers

from models import Server, AdminOptions
import prowlpy
#import twitter

class CheckServers(webapp.RequestHandler):
	serverlist = db.GqlQuery("SELECT * FROM Server")
	adminoptions = AdminOptions.get_by_key_name('credentials')
    
	def updateuptime(self,server):
		now = time.mktime(datetime.datetime.now().timetuple())
		servercameback = time.mktime(server.timeservercameback.timetuple())
		difference = now - servercameback
		MINUTE  = 60
		HOUR    = MINUTE * 60
		DAY     = HOUR * 24
		days    = int( difference / DAY )
		hours   = int( ( difference % DAY ) / HOUR )
		minutes = int( ( difference % HOUR ) / MINUTE )
		seconds = int( difference % MINUTE )

		string = ""
		if days> 0:
			string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
		if len(string)> 0 or hours> 0:
			string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
		if len(string)> 0 or minutes> 0:
			string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
		string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
		server.uptime = string
		server.put()
 
	def serverisup(self,server,responsecode):
		if server.status == False:
			self.servercameback(server)
		server.status = True
		server.falsepositivecheck = False
		server.responsecode = int(responsecode)
		server.uptimecounter = server.uptimecounter + 1
		self.updateuptime(server)
		server.put()
    
	def serverisdown(self,server,responsecode):
		server.status = False
		server.uptimecounter = 0
		server.uptime = "0"
		server.responsecode = int(responsecode)
		server.timeservercameback = 0
		server.put()
		if server.notifylimiter == False:
			if server.notifywithprowl:
				self.notifyprowl(server)
			if server.notifywithemail:
				self.notifyemail(server)
		else:
			pass

	def servercameback(self,server):
		server.timeservercameback = datetime.datetime.now()

	def testserver(self,server):
		if server.ssl:
			prefix = "https://"	
		else:
			prefix = "http://"
		try:
			url = prefix + "%s" % server.serverdomain
			result = urlfetch.fetch(url, headers = {'Cache-Control' : 'max-age=30'}, deadline=10 )
		except DownloadError:
			if server.falsepositivecheck:
				self.serverisdown(server,000)
			else:
				server.falsepositivecheck = True
				server.put()
		else:
			if result.status_code == 500:
				self.serverisdown(server,result.status_code)
			else:
				self.serverisup(server,result.status_code)

	def notifyemail(self,server):
		message = mail.EmailMessage()
		message.sender = server.email
		message.subject = "%s is down" % server.serverdomain
		message.to = server.email
		message.body = "HTTP response code %s" % server.responsecode
		message.send()
		server.notifylimiter = True
		server.put()
					
	def notifytwitter(self,server):
		pass
		#api = twitter.Api(username="%s" % self.adminoptions.twitteruser , password="%s" % self.adminoptions.twitterpass)
		#api.PostDirectMessage(self.adminoptions.twitteruser, "%s is down" % server.serverdomain)
		#server.notifylimiter = True
		#server.put()
		
	def notifyprowl(self,server):
		prowlkey = self.adminoptions.prowlkey
		prowlnotifier = prowlpy.Prowl(prowlkey)
		try:
			prowlnotifier.add('Server Monitor','Server %s is Down' % server.serverdomain, 'error code %s' % server.responsecode)
		except:
			logging.error('prowl notify failed, you may need to check your API key')
		server.notifylimiter = True
		server.put()	
                
	def get(self):
		for server in self.serverlist:
			self.testserver(server)
            
def main():
	application = webapp.WSGIApplication([('/checkservers', CheckServers)],debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
