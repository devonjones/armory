from google.appengine.ext import ndb

from armory.models.account import Account
from armory.models.player import Player
from armory.models.session import Session

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
			retval["current_session"] = cs.to_json()
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

