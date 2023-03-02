#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import pytest
import logging
import allure
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


@pytest.fixture(scope="function", autouse=True)
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get("http://54.201.140.239/index.html")
    yield driver
    driver.quit()


@pytest.fixture
def session():
    session = requests.Session()
    yield session
