import json
import webapp2
from google.appengine.api import users
from armory.models.account import Account

class UserResource(webapp2.RequestHandler):
	def get(self):
		account = Account.get_account(users.get_current_user())
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(account.to_json(), indent=2))

	def post(self):
		data = json.loads(self.request.body)
		account = Account.get_account(users.get_current_user())
		account.name = data["name"]
		account.put()
		self.response.headers["Content-Type"] = "application/json"
		self.response.write("%s\n" % json.dumps(account.to_json(), indent=2))
