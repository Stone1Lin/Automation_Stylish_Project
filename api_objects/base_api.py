#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
import logging
from json.decoder import JSONDecodeError


class BaseAPI:
    def __init__(self, session):
        self.session = session

    def request(self, method, **kwargs):
        # payload = kwargs.get("json", None)
        try:
            return self.session.request(method, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.info(f"Exception:{e}")

        # except JSONDecodeError as e:
        #     logging.info(f"Exception:{e}")
        # logging.info(f"Response: {self.resp}")
        # logging.info(f"headers: {self.resp.headers}")
        # logging.info(f"headers: {self.resp.status_code}")