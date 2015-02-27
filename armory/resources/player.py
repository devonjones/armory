import json
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.models.account import Account
from armory.models.player import Player

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

