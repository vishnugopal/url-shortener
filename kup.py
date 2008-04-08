import cgi
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

class Kupify:
  def kupify_next(previous_pattern):
    if(previous_pattern.endswith("z"))
		  return kupify_next(previous_pattern[1:-1]) + 'a'
		else
      return previous_pattern[1:-1] + chr(ord(previous_pattern[-1]) + 1)
      
class URL(db.Model):
  url = db.IntegerProperty()
  url_id = db.DateTimeProperty(auto_now_add=True)
  kup = db.StringProperty(multiline=True)

class Index(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
        <body>
          <form action="/_" method="post">
            <div><input name="url" id="url" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Kup URL!"></div>
          </form>
        </body>
      </html>""")


class Kup(webapp.RequestHandler):
  def post(self):
    self.response.out.write('<html><body>You wrote:<pre>')
    self.response.out.write(cgi.escape(self.request.get('url')))
    self.response.out.write('</pre></body></html>')

def main():
  application = webapp.WSGIApplication(
                                       [('/', Index),
                                        ('/_', Kup)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()