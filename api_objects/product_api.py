#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from Stylish_Project.api_objects.base_api import BaseAPI


class Prod_SearchAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/products/search"

    def send(self, test_data):
        params = {
            "keyword": test_data['keyword'],
            "paging": test_data['paging']
        }
        return self.request(test_data['Method'], url=self.url, params=params)


class Prod_DetailAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/products/details"

    def send(self, test_data):
        params = {
            "id": test_data['id']
        }
        return self.request(test_data['Method'], url=self.url, params=params)


class Prod_CategoryAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/products/"

    def send(self, test_data):
        params = {
            "paging": test_data['paging']
        }
        self.url = self.url + test_data['category']
        return self.request(test_data['Method'], url=self.url, params=params)
