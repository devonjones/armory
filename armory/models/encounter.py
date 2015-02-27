from google.appengine.ext import ndb

from armory.models.account import Account
from armory.models.session import Session

class Encounter(ndb.Model):
	name = ndb.StringProperty()
	applied = ndb.KeyProperty(kind=Session)
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)

	def to_json(self):
		retval = {
			"id": self.key.id(),
			"name": self.name,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat()
		}
		if self.applied:
			retval["applied"] = self.applied.get().to_json()
		return retval
