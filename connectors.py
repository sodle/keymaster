import requests
import orm
from urllib import urlencode
from flask import redirect, render_template


class Connector(object):
    name = ''
    logo = ''

    def __init__(self):
        pass

    def start_key_install(self):
        pass

    def finish_key_install(self):
        pass


class GitHubConnector(Connector):
    name = 'GitHub'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def start_key_install(self, key_id, callback_url):
        gh_query = {
            'client_id': self.api_key,
            'redirect_uri': callback_url,
            'scope': 'repo,admin:public_key,repo_deployment'
        }
        query_string = urlencode(gh_query)
        url = 'https://github.com/login/oauth/authorize?' + query_string
        return redirect(url)

    def finish_key_install(self, key_id, arguments):
        authorize_url = 'https://github.com/login/oauth/access_token'
        authorize_query = {
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'code': arguments['code']
        }
        authorize_headers = {'Accept': 'application/json'}
        token_obj = requests.post(authorize_url, data=authorize_query,
                                  headers=authorize_headers).json()
        token = token_obj['access_token']

        pub_key = orm.fetch_key(key_id)[2]

        list_repos_url = 'https://api.github.com/user/repos'
        list_repos_query = {
            'access_token': token
        }
        repos = requests.get(list_repos_url,
                             params=list_repos_query).json()

        return render_template('connectors/github/install_key.html',
                               access_token=token,
                               public_key=pub_key,
                               repos=repos
                               )
