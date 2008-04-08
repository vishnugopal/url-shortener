import cgi
import os
import wsgiref.handlers
from urlparse import urlparse

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

class Kupify:
	def next(self, previous_pattern):
		if(previous_pattern == ''):
			return 'a'
		if(previous_pattern == 'z'):
			return 'aa'			
		if(previous_pattern.endswith("z")):
			return self.next(previous_pattern[0:-1]) + 'a'
		else:
			return previous_pattern[0:-1] + chr(ord(previous_pattern[-1]) + 1)

class URL(db.Model):
	url = db.StringProperty()
	url_id = db.IntegerProperty()
	pattern = db.StringProperty()

	def check_already_existing(self, url):
		u = False
		try:
			u = db.GqlQuery("SELECT * from URL WHERE url = :1", url)
			u = u[0]
			return u
		except (IndexError, AttributeError):
			return False
		
	def find_last_url(self):
		u = False
		try:
			u = db.GqlQuery("SELECT * from URL ORDER BY url_id DESC LIMIT 1")[0]
			return u
		except IndexError:
			return False
	
	def url_for_pattern(self, pattern):
		u = False
		try:
			u = db.GqlQuery("SELECT * from URL WHERE pattern = :1 LIMIT 1", pattern)[0]
			return u
		except IndexError:
			return False

class Index(webapp.RequestHandler):
	def get(self):
		template = file(os.path.join(os.path.dirname(__file__), 'index.html'))
		template = template.read()
		self.response.content_type = "text/html; charset=utf8"
		self.response.out.write(template)

class Redirect(webapp.RequestHandler):
	def get(self):
		pattern = self.request.environ['PATH_INFO'][1:].strip()
		
		u = URL()
		url = u.url_for_pattern(pattern)
		if(url):
			self.redirect(url.url)
		else:
			self.response.out.write("Can't find a URL to redirect!")

class Kup(webapp.RequestHandler):
	def post(self):
		u = URL()
		k = Kupify()
		
		next_url = self.request.get('url')
		
		#only if http or https
		scheme = urlparse(next_url)[0]
		if(not (scheme == 'http' or scheme == 'https')):
			self.response.out.write('ERROR')
			return
		
		#if already existing, return that record.
		b = u.check_already_existing(next_url)
		if(b):
			self.response.out.write('http://r.kup.in/' + b.pattern)
			return
			
		last_url = u.find_last_url()
		last_url_pattern = ''
		last_url_id = 0
		try:
			last_url_pattern = last_url.pattern
			last_url_id = last_url.url_id
		except AttributeError:
			pass
			
		next_url_pattern = k.next(last_url_pattern)
		
		u.url = self.request.get('url')
		u.url_id = last_url_id + 1
		u.pattern = next_url_pattern
		u.put()
				
		self.response.out.write('http://r.kup.in/' + next_url_pattern)

def main():
	application = webapp.WSGIApplication(
		[('/', Index),
		('/_', Kup),
		('/.*', Redirect)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()