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


from google.appengine.ext import db

class Server(db.Model):
	serverdomain = db.StringProperty("Server Domain", multiline=False)
	ssl = db.BooleanProperty("Is server SSL?", default=False)
	email = db.EmailProperty("Email Address for notification")
	startedmonitoring = db.DateTimeProperty("Date monitoring started", auto_now_add=True)
	timeservercameback = db.DateTimeProperty("Date server came back online", auto_now_add=True)
	status = db.BooleanProperty("Server Status", default=False)
	responsecode = db.IntegerProperty("Server response code", default=000)
	notifylimiter = db.BooleanProperty("Notify limiter", default=False)
	uptimecounter = db.IntegerProperty("Uptime Counter", default=0)
	notifywithprowl = db.BooleanProperty("Prowl notifications",default=False)
	notifywithemail = db.BooleanProperty("Email notifications",default=False)
	notifywithtwitter = db.BooleanProperty("Twitter notifications",default=False)
	notifywithfacebook = db.BooleanProperty("Facebook notifications",default=False)
	notifywithsms = db.BooleanProperty("SMS notifications",default=False)
	falsepositivecheck = db.BooleanProperty("Prevent single bad result from triggering notifications",default=False)
	uptime = db.StringProperty("Uptime")
	class Uptime(db.Model):
		unittime = db.DateTimeProperty("Time period for uptime data", auto_now_add=False)
		uptimecounter = db.IntegerProperty("Counter for uptime in minutes for the time period", default=0)
		downtimecounter = db.IntegerProperty("Counter for downtime in minutes for the time period", default=0)
    
class AdminOptions(db.Model):
	twitteruser = db.StringProperty("Twitter Username", multiline=False)
	twitterpass = db.StringProperty("Twitter Passowrd", multiline=False)
	facebookconnect = db.StringProperty("Facebook connect", multiline=False)
	mobilesmsnumber = db.StringProperty("Mobile SMS number", multiline=False)
	prowlkey = db.StringProperty("Prowl API Key", multiline=False)
	prowlkeyisvalid = db.BooleanProperty("Prowl key status", default=False)
