from google.appengine.ext import ndb

from armory.models.account import Account

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
