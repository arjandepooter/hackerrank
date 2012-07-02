# -*- coding: utf-8 -*-
from requests import Session
from lxml import html
import json

BASE_URL = 'https://www.hackerrank.com'

class HackerrankSession(Session):
    def __init__(self, *args, **kwargs):
        super(HackerrankSession, self).__init__(*args, **kwargs)

        res = self.get('/')
        etree = html.fromstring(res.content)
        self.headers['X-CSRF-Token'] = etree.xpath('/html/head/meta[@name="csrf-token"]')[0].attrib['content']

    def login(self, username, password):
        res = self.post('/users/sign_in.json', data={
            'commit' : 'Sign in',
            'user[login]' : username,
            'user[password]' : password, 
        })
        if 'error' in res:
            raise Exception(res['error'])
        return res

    def request(self, method, path, *args, **kwargs):
        kwargs['url'] = '%s%s' % (BASE_URL, path)
        res = super(HackerrankSession, self).request(method, *args, **kwargs)
        if 'content-type' in res.headers and 'application/json' in res.headers['content-type'].split('; '):
            return json.loads(res.content)
        return res
