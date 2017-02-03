#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import cgi
import re
import fnmatch

html="""
<form method="post">
    <font><h1>Signup<h1></font>
    <table>
        <tr>
            <td><b>Username</b></td>
            <td><input name = "username" value = "%(user)s"/></td>
            <td style = "color: red">%(error_username)s</td>
        </tr>
        <tr>
            <td><b>Password</b></td>
            <td><input type = "password" name = "password" value = ""/></td>
            <td style = "color: red">%(error_password1)s</td>
        </tr>
        <tr>
            <td><b>Verify Password</b></td>
            <td><input type = "password" name = "verify_pw" value = ""/></td>
            <td style="color: red">%(error_password2)s</td>
        </tr>
        <tr>
            <td><b>Email (optional)</b></td>
            <td><input name = "email" value = "%(email)s"/></td>
            <td style = "color: red">%(error_email)s</td>
        </tr>
    </table>
    <input type = "submit" name = "submit" value = "Submit">
</form>
"""

def valid_uname(user):
    if user is None:
        return user

def escape_html(s):
    return cgi.escape(s, quote=True)

uname_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
pw_check = re.compile(r"^.{3,20}$")
email_check = re.compile(r"^[\S]+@[\S]+.[\S]+$")

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_username="", error_password1="", error_password2="", error_email="", user="", email=""):
        self.response.out.write(html % {'error_username': error_username,
                                        'error_password1': error_password1,
                                        'error_password2': error_password2,
                                        'error_email': error_email,
                                        'user': escape_html(user),
                                        'email': escape_html(email)
                                        })

    def get(self):
        self.write_form()

    def post(self):
        user = self.request.get('username')
        user_pw = self.request.get('password')
        user_verify_pw = self.request.get('verify_pw')
        email = self.request.get('email')
        email_check = '*@*.*'
        has_error = False

        if not (user and uname_check.match(user)):
            error_username = "That's not a valid username"
            has_error = True
        else:
            error_username = ""

        if not (user_pw and pw_check.match(user_pw)):
            error_password1 = "That's not a valid password"
            has_error = True
        else:
            error_password1 = ""

        if user_pw != user_verify_pw or (not user_pw or not user_verify_pw):
            error_password2 = "Passwords do not match"
            has_error = True
        else:
            error_password2 = ""

        if email != "" and not fnmatch.fnmatch(email, email_check):
            error_email = "Invalid email address"
            has_error = True
        else:
            error_email = ""

        if has_error == True:
             self.write_form(error_username, error_password1, error_password2, error_email, user, email)
        else:
            self.redirect('/welcome?username=' + user)

class Welcome(webapp2.RequestHandler):
    def get(self):
        user = escape_html(self.request.get('username'))
        self.response.write('<h1>Welcome, ' + user + '!</h1>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome),
], debug=True)
