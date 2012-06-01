## App Engine Server Monitor

This is a web server monitor written to run on Google App Engine. It's quite old but it still works and is being actively used by the original author 24/7. 

The interface does not use Ajax, there is nothing but a form for adding new domains to monitor, and a list of servers being monitored. Most of the magic happens in checkservers.py which is used by the App Engine cron system to periodically check the stored domains.

### Notifications

The notification method is via email or Prowl, which is a custom push notification API for iOS devices. I typically use email though, as I get iPhone notifications for those anyway.


