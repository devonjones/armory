import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.models.account import Account
from armory.models.encounter import Encounter

class EncountersResource(webapp2.RequestHandler):
	def get(self, campaign_id):
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
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		encounters = []
		r = Encounter.query(ancestor=campaign.key).fetch()
		for encounter in r:
			encounters.append(encounter.to_json())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(encounters, indent=2))

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
		r = Encounter.query(ancestor=campaign.key).fetch()
		new_encounter = Encounter(
			name=data["name"],
			parent=campaign.key)
		new_encounter.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(new_encounter.to_json(), indent=2))
		return

class EncounterResource(webapp2.RequestHandler):
	def get(self, campaign_id, encounter_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		ek = ndb.Key(
			"Campaign", int(campaign_id),
			"Encounter", int(encounter_id))
		encounter = ek.get()
		if campaign == None or encounter == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to see this object"},
				indent=2))
			return
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(encounter.to_json(), indent=2))

	def post(self, campaign_id, encounter_id):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		ek = ndb.Key(
			"Campaign", int(campaign_id),
			"Encounter", int(encounter_id))
		encounter = ek.get()
		if campaign == None or encounter == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to modify this object"},
				indent=2))
			return
		encounter.name = data["name"]
		encounter.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(encounter.to_json(), indent=2))

	def delete(self, campaign_id, encounter_id):
		account = Account.get_account(users.get_current_user())
		key = ndb.Key("Campaign", int(campaign_id))
		campaign = key.get()
		ek = ndb.Key(
			"Campaign", int(campaign_id),
			"Encounter", int(encounter_id))
		encounter = ek.get()
		if campaign == None or encounter == None:
			self.response.status = 404
			return
		if not campaign.admin_access_allowed(account):
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "You don't have permission to delete this object"},
				indent=2))
			return
		if encounter.applied:
			self.response.status = 403
			self.response.headers["Content-Type"] = "application/json"
			self.response.write("%s\n" % json.dumps(
				{"error": "Can't delete an encounter that is already applied"},
				indent=2))
			return
		#TODO: block from deleting a encounter if it's in use.
		encounter.key.delete()
		self.response.status = 204

