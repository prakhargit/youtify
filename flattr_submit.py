# -*- coding: utf-8 -*-

import os
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import users
from django.utils import simplejson
from model import get_current_youtify_user
from model import create_youtify_user

class Handler(webapp.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        user = get_current_youtify_user()
        if (current_user is not None) and (user is None):
            user = create_youtify_user()

        logout_url = ''
        login_url = ''
        my_user_email = ''
        my_flattr_username = ''
        if (user is not None):
            my_user_email = user.google_user.email()
            logout_url = users.create_logout_url('/flattr_submit')
            if user.flattr_user_name:
                my_flattr_username = user.flattr_user_name
        else:
            login_url = users.create_login_url('/flattr_submit')

        path = os.path.join(os.path.dirname(__file__), 'html', 'flattr_submit.html')
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write(template.render(path, {
            'my_user_email': my_user_email,
            'my_flattr_username': my_flattr_username,
            'logout_url': logout_url,
            'flattr_connect_url': '/flattrconnect?redirect_uri=' + urllib.quote(self.request.url),
            'flattr_disconnect_url': '/flattrdisconnect?redirect_uri=' + urllib.quote(self.request.url),
            'login_url': login_url,
        }))

    def post(self):
        ret = {
            'css_class': 'ok',
            'message': 'Thing submitted',
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps(ret))

def main():
    application = webapp.WSGIApplication([
        ('/flattr_submit', Handler),
    ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()