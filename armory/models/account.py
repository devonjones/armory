from google.appengine.ext import ndb

class Account(ndb.Model):
	user_id = ndb.StringProperty()
	email = ndb.StringProperty()
	name = ndb.StringProperty()

	def to_json(self):
		retval = {
			"email": self.email,
			"name": self.name
		}
		return retval

	@classmethod
	def get_account(cls, user):
		q = cls.query(Account.user_id == user.user_id())
		r = q.fetch(1)
		if len(r) > 0:
			return r[0]
		else:
			sys.stderr.write("%s\n" % dir(user))
			new_account = Account(
				user_id=user.user_id(),
				email=user.email(),
				name=user.nickname())
			new_account.put()
			return new_account

	@classmethod
	def get_name(cls, user):
		account = Account.get_account(user)
		return account.name
