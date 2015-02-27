from google.appengine.ext import ndb

from armory.models.account import Account

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
