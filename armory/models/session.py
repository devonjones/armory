from google.appengine.ext import ndb

class Session(ndb.Model):
	name = ndb.StringProperty()
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)

	def to_json(self):
		retval = {
			"id": self.key.id(),
			"name": self.name,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat()
		}
		return retval
