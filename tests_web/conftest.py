#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pytest
import logging
import allure
from configparser import ConfigParser
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

driver_type = "chrome"
driver = None

# [TODO] Using custom option to get test env
# def pytest_addoption(parser):
#     parser.addoption(
#         '--env', action='store', default='http://54.201.140.239/index.html', help='Base URL for the tests'
#     )
#
#
# @pytest.fixture
# def test_env(request):
#     return request.config.getoption('--env')

@pytest.fixture(scope="function", autouse=True)
def driver():
    """
    定義全域瀏覽器驅動
    :return:
    """
    global driver
    global driver_type

    if driver_type == "chrome":
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    elif driver_type =="firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise NameError("driver_type 不支援.")
    driver.maximize_window()
    driver.get("http://54.201.140.239/index.html")
    yield driver
    driver.quit()

    # opt = Options()
    # opt.add_argument("--window-size=1920,1080")
    # opt.add_argument("--ignore-ssl-errors=yes")
    # opt.add_argument('--ignore-certificate-errors')
    # opt.add_argument("--no-sandbox")
    # driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=opt)
    # driver.maximize_window()
    # yield driver
    # driver.quit()

def pytest_collection_modifyitems(items):
    """
    測試 case 收集完成時，將收集到的item的 name 和 node_id 的中文顯示在控制檯上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call':
        if hasattr(driver, "get_screenshot_as_png"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )


# @pytest.fixture(autouse=True)
# def get_ini(pytestconfig):
#     # Read ini info
#     # Read log_cli info
#     log_cli = pytestconfig.getini("log_cli")
#     print(f"Get markers: {log_cli}")
#     addopts = pytestconfig.getini("addopts")
#     print(f"Get addopts: {addopts}")

# @pytest.fixture(scope="function", autouse=True)
# def base_driver(driver):
#     return BasePage(driver)


