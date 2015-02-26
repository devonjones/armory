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

class BasePage(object):
	def cant_see(self):
		self.response.status = 403
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(
			{"error": "You don't have permission to see this object"},
			indent=2))

	def cant_modify(self):
		self.response.status = 403
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(
			{"error": "You don't have permission to modify this object"},
			indent=2))

	def cant_delete(self):
		self.response.status = 403
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(
			{"error": "You don't have permission to delete this object"},
			indent=2))

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
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
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
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to modify this object"},
				indent=2))
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
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to delete this object"},
				indent=2))
			return
		campaign.key.delete()
		self.response.status = 204

class PlayersResource(webapp2.RequestHandler):
	def get(self, campaign_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		players = []
		r = Player.query(ancestor=campaign.key).fetch()
		for player in r:
			players.append(player.to_json())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(players, indent=2))

class PlayerResource(webapp2.RequestHandler):
	def get(self, campaign_id, player_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		pk = ndb.Key("Campaign", int(campaign_id), "Player", int(player_id))
		player = pk.get()
		if campaign == None or player == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			if player.account != account.key:
				self.response.status = 403
				self.response.headers["Content-Type"] = "application/json"
				self.response.write("%s\n" % json.dumps(
					{"error": "You don't have permission to see this object"},
					indent=2))
				return
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(player.to_json(), indent=2))

	def post(self, campaign_id, player_id):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		pk = ndb.Key("Campaign", int(campaign_id), "Player", int(player_id))
		player = pk.get()
		if campaign == None or player == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			if player.account != account.key:
				self.response.status = 403
				self.response.headers["Content-Type"] = "application/json"
				self.response.write("%s\n" % json.dumps(
					{"error": "You don't have permission to modify this object"},
					indent=2))
				return
		player.character_name = data["character_name"]
		player.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(player.to_json(), indent=2))

	def delete(self, campaign_id, player_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		pk = ndb.Key("Campaign", int(campaign_id), "Player", int(player_id))
		player = pk.get()
		if campaign == None or player == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			if player.account != account.key:
				self.response.status = 403
				self.response.headers["Content-Type"] = "application/json"
				self.response.write("%s\n" % json.dumps(
					{"error": "You don't have permission to delete this object"},
					indent=2))
				return
		player.key.delete()
		self.response.status = 204

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
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to delete this object"},
				indent=2))
			return
		campaign.token=str(uuid.uuid4())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(campaign.to_json(), indent=2))

class SessionsResource(webapp2.RequestHandler):
	def get(self, campaign_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		sessions = []
		r = Session.query(ancestor=campaign.key).order(Session.created_at).fetch()
		for session in r:
			sessions.append(session.to_json())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(sessions, indent=2))

	def post(self, campaign_id):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to modify this object"},
				indent=2))
			return
		r = Session.query(ancestor=campaign.key).fetch()
		name = data.get("name", "Session %s" % (len(r) + 1))
		new_session = Session(
			name=name,
			parent=campaign.key)
		new_session.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(new_session.to_json(), indent=2))
		return

class SessionResource(webapp2.RequestHandler):
	def get(self, campaign_id, session_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		sk = ndb.Key("Campaign", int(campaign_id), "Session", int(session_id))
		session = sk.get()
		if campaign == None or session == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(session.to_json(), indent=2))

	def post(self, campaign_id, session_id):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		sk = ndb.Key("Campaign", int(campaign_id), "Session", int(session_id))
		session = sk.get()
		if campaign == None or session == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to modify this object"},
				indent=2))
			return
		session.name = data["name"]
		session.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(session.to_json(), indent=2))

	def delete(self, campaign_id, session_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		sk = ndb.Key("Campaign", int(campaign_id), "Session", int(session_id))
		session = sk.get()
		if campaign == None or session == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to delete this object"},
				indent=2))
			return
		if campaign.current_session() != session:
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "Only current session can be deleted"}, indent=2))
			return
		#TODO: block from deleting a session if it's in use.
		session.key.delete()
		self.response.status = 204

class NotesResource(webapp2.RequestHandler):
	def get(self, campaign_id, session_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		if campaign == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		notes = []
		sk = ndb.Key("Campaign", int(campaign_id), "Session", int(session_id))
		r = Note.query(ancestor=sk).order(Session.created_at).fetch()
		for note in r:
			if campaign.admin_access_allowed(account) or note.public:
				notes.append(note.to_json())
			elif account.key == note.account:
				notes.append(note.to_json())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(notes, indent=2))

	def post(self, campaign_id, session_id):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		sk = ndb.Key("Campaign", int(campaign_id), "Session", int(session_id))
		session = sk.get()
		if campaign == None or session == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to modify this object"},
				indent=2))
			return
		new_note = Note(
			account=account.key,
			public=data.get("public", True),
			note=data["note"],
			parent=sk)
		if data.has_key("name"):
			new_note.name = data["name"]
		new_note.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(new_note.to_json(), indent=2))

class NoteResource(webapp2.RequestHandler):
	def get(self, campaign_id, session_id, note_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		nk = ndb.Key(
			"Campaign", int(campaign_id),
			"Session", int(session_id),
			"Note", int(note_id))
		note = nk.get()
		if campaign == None or note == None:
			self.response.status = 404
			return
		if not campaign.access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		if not campaign.admin_access_allowed(account):
			if not note.public:
				if not account.key == note.account:
					self.response.status = 403
					self.response.headers["Content-Type"] = "application/json"
					self.response.write("%s\n" % json.dumps(
						{"error": "You don't have permission to see this object"},
						indent=2))
					return
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(note.to_json(), indent=2))

	def post(self, campaign_id, session_id, note_id):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		nk = ndb.Key(
			"Campaign", int(campaign_id),
			"Session", int(session_id),
			"Note", int(note_id))
		note = nk.get()
		if campaign == None or note == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			if not account.key == note.account:
				self.response.status = 403
				self.response.headers["Content-Type"] = "application/json"
				self.response.write("%s\n" % json.dumps(
					{"error": "You don't have permission to modify this object"},
					indent=2))
				return
		if data.has_key("name"):
			note.name = data["name"]
		if data.has_key("public"):
			note.public = data["public"]
		if data.has_key("note"):
			note.note = data["note"]
		note.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(note.to_json(), indent=2))

	def delete(self, campaign_id, session_id, note_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		nk = ndb.Key(
			"Campaign", int(campaign_id),
			"Session", int(session_id),
			"Note", int(note_id))
		note = nk.get()
		if campaign == None or note == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			if not account.key == note.account:
				self.response.status = 403
				self.response.headers["Content-Type"] = "application/json"
				self.response.write("%s\n" % json.dumps(
					{"error": "You don't have permission to modify this object"},
					indent=2))
				return
		note.key.delete()
		self.response.status = 204

application = webapp2.WSGIApplication([
	(r'/', MainPage),
	(r'/campaigns', CampaignsResource),
	(r'/campaigns/token', CampaignsTokenResource),
	(r'/campaigns/(\d+)', CampaignResource),
	(r'/campaigns/(\d+)/token', CampaignTokenResource),
	(r'/campaigns/(\d+)/players', PlayersResource),
	(r'/campaigns/(\d+)/players/(\d+)', PlayerResource),
	(r'/campaigns/(\d+)/sessions', SessionsResource),
	(r'/campaigns/(\d+)/sessions/(\d+)', SessionResource),
	(r'/campaigns/(\d+)/sessions/(\d+)/notes', NotesResource),
	(r'/campaigns/(\d+)/sessions/(\d+)/notes/(\d+)', NoteResource),
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
		for player in self.players():
			retval["players"].append(player.to_json())
		cs = self.current_session()
		if cs:
			retval["current_session"] = cs
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

	def current_session(self):
		r = Session.query(ancestor=self.key).order(-Session.created_at).fetch(1)
		for session in r:
			return session

	def players(self):
		players = []
		r = Player.query(ancestor=self.key).fetch()
		for player in r:
			players.append(player)
		return players

class Session(ndb.Model):
	name = ndb.StringProperty()
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)

	def to_json(self):
		retval = {
			"id": self.key.id(),
			"name": self.name,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat()
		}
		return retval

class Note(ndb.Model):
	account = ndb.KeyProperty(kind=Account)
	name = ndb.TextProperty()
	note = ndb.TextProperty()
	public = ndb.BooleanProperty()
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)

	def to_json(self):
		account = self.account.get()
		retval = {
			"id": self.key.id(),
			"owner": account.name,
			"name": self.name,
			"note": self.note,
			"public": self.public,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat()
		}
		return retval

