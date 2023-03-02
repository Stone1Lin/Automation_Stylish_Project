#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import json
from Stylish_Project.api_objects.base_api import BaseAPI


class OrderAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/order"

    def send(self, test_data):
        payload = {
            "prime": test_data['prime'],
            "order": {
                "shipping": "delivery",
                "payment": "credit_card",
                "subtotal": int(test_data['Subtotal']),
                "freight": int(test_data['Freight']),
                "total": int(test_data['Total']),
                "recipient": {
                    "name": test_data['Receiver'],
                    "phone": test_data['Mobile'],
                    "email": test_data['Email'],
                    "address": test_data['Address'],
                    "time": test_data['Deliver Time']
                },
                "list": json.loads(test_data['list'])
            }
        }
        logging.info(f"payload: {payload}")
        return self.request(test_data['Method'], url=self.url, json=payload)


class GetOrderAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/order/"

    def send(self, order_number):
        return self.request("get", url=self.url+order_number)
