import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.models.account import Account
from armory.models.session import Session

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

