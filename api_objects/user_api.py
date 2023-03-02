#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
from dotenv import load_dotenv, find_dotenv
from Stylish_Project.api_objects.base_api import BaseAPI

load_dotenv(".env")
load_dotenv(find_dotenv())


class LoginAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/user/login"

    def _send(self, test_data):
        payload = {
            "provider": test_data['Provider'],
            "email": test_data['Email'],
            "password": test_data['Password']
        }
        return self.request(test_data['Method'], url=self.url, json=payload)

    def get_login_info(self):
        payload = {"Method": "POST", "Provider": "native", "Email": os.getenv("login_email"),
                   "Password": os.getenv("login_pw")}
        resp = self._send(payload)
        access_token = resp.json()['data']['access_token']
        user_id = resp.json()['data']['user']['id']
        self.session.headers = {"Authorization": f"Bearer {access_token}"}
        return access_token, user_id

    def set_login_auth(self, access_token):
        if access_token != "":
            self.session.headers = {"Authorization": f"Bearer {access_token}"}
        else:
            self.session.headers = {}


class LogoutAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/user/logout"

    def _send(self):
        return self.request("post", url=self.url)


class ProfileAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/user/profile"

    def _send(self):
        return self.request("get", url=self.url)