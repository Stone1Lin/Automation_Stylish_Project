#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests


class DebugTalk:
    def check_url_exists(self, url: str):
        """
        Checks if a url exists
        :param url: url to check
        :return: True if the url exists, false otherwise.
        """
        return requests.head(url, allow_redirects=True).status_code == 200


if __name__ == '__main__':
    url = "http://54.201.140.239/assets/201807201824/main.jpg"
    test = requests.head(url, allow_redirects=True).status_code == 200
    print(test)