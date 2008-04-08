import cgi
import wsgiref.handlers
from urlparse import urlparse

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

class Kupify:
	def next(self, previous_pattern):
		if(previous_pattern == 'z'):
			return 'aa'
		if(previous_pattern == ''):
			return 'a'			
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
			uid = u.url_id
			return u
		except IndexError:
			return False
		except AttributeError:
			return False
		
	def find_last_url(self):
		u = False
		try:
			u = db.GqlQuery("SELECT * from URL ORDER BY url_id DESC LIMIT 1")
			u = u[0]
		except IndexError:
			pass
		return u

class Index(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""
		<html>
		<body>
		<form action="/_" method="post">
		<div><input name="url" id="url" rows="3" cols="60"></div>
		<div><input type="submit" value="Kup URL!"></div>
		</form>
		</body>
		</html>""")

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
			u = b
			out = ''
			out += '<html><body>URL:<pre>'
			out += cgi.escape(u.url)
			out += '</pre><br>Already existing ID:<pre>'
			out += str(u.url_id)
			out += '</pre><br>Already existing Pattern:<pre>'
			out += 'http://kup.in/' + u.pattern
			out += '</pre></body></html>'
			self.response.out.write(out)
			return
			
		last_url = u.find_last_url()
		last_url_pattern = ''
		last_url_id = 0
		try:
			last_url_pattern = last_url.pattern
			last_url_id = last_url.url_id
		except AttributeError:
			pass
			
		next_pattern = k.next(last_url_pattern)
		
		u.url = self.request.get('url')
		u.url_id = last_url_id + 1
		u.pattern = next_pattern
		u.put()
		
		out = ''
		out += '<html><body>URL:<pre>'
		out += cgi.escape(self.request.get('url'))
		out += '</pre><br>Last Pattern ID:<pre>'
		out += str(last_url_id)
		out += '</pre><br>Last Pattern:<pre>'
		out += 'http://kup.in/' + last_url_pattern
		out += '</pre><br>Pattern:<pre>'
		out += 'http://kup.in/' + next_pattern
		out += '</pre></body></html>'
		
		self.response.out.write(out)

def main():
	application = webapp.WSGIApplication(
		[('/', Index),
		('/_', Kup)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()