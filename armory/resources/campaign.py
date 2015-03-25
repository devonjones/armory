import json
import uuid
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.models.account import Account
from armory.models.campaign import Campaign

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
