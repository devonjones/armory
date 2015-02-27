import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.models.account import Account
from armory.models.session import Session
from armory.models.note import Note

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

