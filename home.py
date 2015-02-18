import os
import sys
import urllib
import json

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			template_values = {
				'url': url,
				'url_linktext': url_linktext
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			template_values = {
				'url': url,
				'url_linktext': url_linktext
			}
			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render(template_values))

class UserResource(webapp2.RequestHandler):
	def get(self):
		account = Account.get_account(users.get_current_user())
		sys.stderr.write("==%s==" % account)
		user = {
			"email": account.email,
			"name": account.name
		}
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(user, indent=2))

	def post(self):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		account.name = data["name"]
		account.put()
		user = {
			"email": account.email,
			"name": account.name
		}
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(user, indent=2))

class CampaignsResource(webapp2.RequestHandler):
	def get(self):
		q = Campaign.query(Campaign.owner_id == users.get_current_user().user_id())

	def post(self):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		account.name = data["name"]
		account.put()
		user = {
			"email": account.email,
			"name": account.name
		}
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(user, indent=2))

class CampaignResource(webapp2.RequestHandler):
	def get(self):
		pass

	def post(self):
		pass

	def delete(self):
		pass

application = webapp2.WSGIApplication([
	(r'/', MainPage),
	(r'/campaigns', CampaignsResource),
	(r'/campaigns/(\d+)', CampaignResource),
	(r'/user', UserResource)
], debug=True)

class Account(ndb.Model):
	user_id = ndb.StringProperty()
	email = ndb.StringProperty()
	name = ndb.StringProperty()

	@classmethod
	def get_account(cls, user):
		q = cls.query(Account.user_id == user.user_id())
		r = q.fetch(1)
		if len(r) > 0:
			return r[0]
		else:
			sys.stderr.write("%s\n" % dir(user))
			new_account = Account(
				user_id=user.user_id(),
				email=user.email(),
				name=user.nickname())
			new_account.put()
			q = cls.query(Account.user_id == user.user_id())
			return q.fetch(1)[0]

	@classmethod
	def get_name(cls, user):
		account = Account.get_account(user)
		return account.name

class Player(ndb.Model):
	user_id = ndb.StringProperty()
	character_name = ndb.StringProperty()

class Campaign(ndb.Model):
	name = ndb.StringProperty()
	owner_id = ndb.StringProperty()
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)
	join_token = ndb.StringProperty()
	players = ndb.StructuredProperty(Player, repeated=True)




class UserNamePage(webapp2.RequestHandler):
	def post(self):
		name = self.request.get('name')
		q = Account.query(Account.user_id == users.get_current_user().user_id())
		r = q.fetch(1)
		if len(r) > 0:
			r[0].name = name
			r[0].put()
		self.redirect('/')
