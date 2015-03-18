import json
import uuid
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.models.account import Account
from armory.models.campaign import Campaign
from armory.models.player import Player

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

