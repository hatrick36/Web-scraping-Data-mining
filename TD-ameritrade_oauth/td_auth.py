import requests
import time
import urllib
from urllib import parse
from splinter import Browser
from variables import *
import os


class td_auth(object):
    def __init__(self, client_id, account_num, password):
        self.password = password
        self.client_id = client_id
        self.account_num = account_num
        self.access_code = None
        self.access_token = None

    def get_access_code(self, client_id):
        driver = {'chromedriver.exe'}
        browser = Browser('chrome', driver, headless=False)
        # define components of url
        method = 'GET'
        url = 'https://auth.tdameritrade.com/auth?'
        client_code = client_id + '@AMER.OAUTHAP'
        payload = {'response_type': 'code', 'redirect_uri': 'http://32.211.92.157', 'client_id': client_code}
        # build url
        my_url = requests.Request(method, url, params=payload).prepare()
        my_url = my_url.url
        browser.visit(my_url)
        # login
        payload = {'username0': user_id, 'password': password}
        browser.find_by_id('username0').first.fill(payload['username0'])
        time.sleep(1)
        browser.find_by_id('password').first.fill(payload['password'])
        time.sleep(1)
        browser.find_by_id('accept').first.click()
        time.sleep(1)
        browser.find_by_text("Can't get the text message?").first.click()
        browser.find_by_value('Answer a security question').first.click()
        # answer security questions
        if browser.is_text_present('What was the name of your high school?'):
            browser.find_by_id('secretquestion0').first.fill('East Lyme High School')

        elif browser.is_text_present('What was your high school mascot?'):
            browser.find_by_id('secretquestion0').first.fill('The Vikings')

        elif browser.is_text_present('What was the name of your first pet?'):
            browser.find_by_id('secretquestion0').first.fill('Cody')
        elif browser.is_text_present(
                'What was the name of the town your grandmother lived in? (Enter full name of town only.)'):
            browser.find_by_id('secretquestion0').first.fill('Scranton')
        browser.find_by_id('accept').first.click()
        time.sleep(1)
        browser.find_by_id('accept').first.click()
        # parse url
        time.sleep(1)
        new_url = browser.url
        access_code = urllib.parse.unquote(new_url.split('code=')[1])
        # close browser
        browser.quit()
        self.access_code = access_code
        print('access_code:', access_code)

        return access_code

    def get_access_token(self):
        # define endpoint
        url = r'https://api.tdameritrade.com/v1/oauth2/token'
        headers = {'Context-Type': 'application/x-www-form-urlencoded'}
        payload = {'grant_type': 'authorization_code',
                   'access_type': 'offline',
                   'code': self.access_code,
                   'client_id': client_id,
                   'redirect_uri': 'http://32.211.92.157'}
        # post data for token
        authreply = requests.post(url, headers=headers, data=payload)
        # convert json-dict
        decoded_content = authreply.json()
        print(decoded_content)

        access_token = decoded_content['access_token']
        os.environ['td_token'] = str(access_token)
        self.access_token = access_token

        return access_token

    def authenticate(self):
        try:
            self.access_token = os.environ['td_token']
        except KeyError:
            self.get_access_code(client_id)
            self.get_access_token()


if __name__ == '__main__':
    td_auth = td_auth(client_id, account_num, password)
    td_auth.authenticate()
