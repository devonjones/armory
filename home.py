import os
import sys
import urllib
import json
import uuid

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
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(account.to_json(), indent=2))

	def post(self):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		account.name = data["name"]
		account.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(account.to_json(), indent=2))

class CampaignsResource(webapp2.RequestHandler):
	def get(self):
		account = Account.get_account(users.get_current_user())
		q = Campaign.query(
				Campaign.owner == account.key)
		r = q.fetch()
		campaigns = []
		for c in r:
			campaigns.append(c.to_json())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(campaigns, indent=2))

	def post(self):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		new_campaign = Campaign(
			name=data["name"],
			owner=account.key,
			token=str(uuid.uuid4()))
		new_campaign.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(
			new_campaign.to_json(), indent=2))

class CampaignsTokenResource(webapp2.RequestHandler):
	def post(self):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		q = Campaign.query(
				Campaign.token == data["token"])
		r = q.fetch(1)
		if len(r) > 0:
			campaign = r[0]
			if campaign.owner == account.key:
				self.response.status = 403
				self.response.headers["Content-Type"] = "application/json"
				self.response.write("%s\n" % json.dumps(
					{"error": "Can't join a campaign you are the GM of"}, indent=2))
				return
			r = Player.query(ancestor=campaign.key).fetch()
			for player in r:
				if player.account == account.key:
					self.response.status = 403
					self.response.headers["Content-Type"] = "application/json"
					self.response.write("%s\n" % json.dumps(
						{"error": "Already a member of campaign"}, indent=2))
					return
			new_player = Player(
				account=account.key,
				character_name=data.get("character_name"),
				parent=campaign.key)
			new_player.put()
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(campaign.to_json(), indent=2))
			return
		else:
			self.response.status = 404

class CampaignResource(webapp2.RequestHandler):
	def get(self, campaign_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			return
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(campaign.to_json(), indent=2))

	def post(self, campaign_id):
		account = Account.get_account(users.get_current_user())
		data = json.loads(self.request.body)
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			return
		campaign.name = data["name"]
		campaign.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(campaign.to_json(), indent=2))

	def delete(self, campaign_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			return
		campaign.key.delete()
		self.response.status = 204

class CampaignTokenResource(webapp2.RequestHandler):
	def delete(self, campaign_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			return
		campaign.token=str(uuid.uuid4())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(campaign.to_json(), indent=2))

application = webapp2.WSGIApplication([
	(r'/', MainPage),
	(r'/campaigns', CampaignsResource),
	(r'/campaigns/token', CampaignsTokenResource),
	(r'/campaigns/(\d+)', CampaignResource),
	(r'/campaigns/(\d+)/token', CampaignTokenResource),
	(r'/user', UserResource)
], debug=True)

class Account(ndb.Model):
	user_id = ndb.StringProperty()
	email = ndb.StringProperty()
	name = ndb.StringProperty()

	def to_json(self):
		retval = {
			"email": self.email,
			"name": self.name
		}
		return retval

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
			return new_account

	@classmethod
	def get_name(cls, user):
		account = Account.get_account(user)
		return account.name

class Player(ndb.Model):
	account = ndb.KeyProperty(kind=Account)
	character_name = ndb.StringProperty()
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)

	def to_json(self):
		account = self.account.get()
		retval = {
			"id": self.key.id(),
			"character_name": self.character_name,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat(),
			"name": account.name,
			"email": account.email
		}
		return retval

class Campaign(ndb.Model):
	name = ndb.StringProperty()
	owner = ndb.KeyProperty(kind=Account)
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)
	token = ndb.StringProperty()

	def to_json(self):
		retval = {
			"id": self.key.id(),
			"name": self.name,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat(),
			"token": self.token,
			"gm": self.owner.get().name,
			"players": []
		}
		r = Player.query(ancestor=self.key).fetch()
		for player in r:
			retval["players"].append(player.to_json())
		return retval

	def admin_access_allowed(self, account):
		if self.owner == account.key:
			return True
		return False

	def access_allowed(self, account):
		if self.owner == account.key:
			return True
		r = Player.query(ancestor=self.key).fetch()
		for player in r:
			if player.account == account.key:
				return True
		return False
