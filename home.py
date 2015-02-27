import os
import sys
import urllib
import json
import uuid
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from armory.resources.user import UserResource
from armory.resources.campaign import CampaignsResource, CampaignResource
from armory.resources.campaign_token import CampaignsTokenResource, CampaignTokenResource
from armory.resources.encounter import EncountersResource, EncounterResource
from armory.resources.player import PlayersResource, PlayerResource
from armory.resources.session import SessionsResource, SessionResource
from armory.resources.note import NotesResource, NoteResource

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			template_values = {
				'url': url,
				'url_linktext': url_linktext
			}
			template = JINJA_ENVIRONMENT.get_template('index.html')
			self.response.write(template.render(template_values))
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			template_values = {
				'url': url,
				'url_linktext': url_linktext
			}
			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
	(r'/', MainPage),
	(r'/campaigns', CampaignsResource),
	(r'/campaigns/token', CampaignsTokenResource),
	(r'/campaigns/(\d+)', CampaignResource),
	(r'/campaigns/(\d+)/token', CampaignTokenResource),
	(r'/campaigns/(\d+)/encounters', EncountersResource),
	(r'/campaigns/(\d+)/encounters/(\d+)', EncounterResource),
	(r'/campaigns/(\d+)/players', PlayersResource),
	(r'/campaigns/(\d+)/players/(\d+)', PlayerResource),
	(r'/campaigns/(\d+)/sessions', SessionsResource),
	(r'/campaigns/(\d+)/sessions/(\d+)', SessionResource),
	(r'/campaigns/(\d+)/sessions/(\d+)/notes', NotesResource),
	(r'/campaigns/(\d+)/sessions/(\d+)/notes/(\d+)', NoteResource),
	(r'/user', UserResource)
], debug=True)

