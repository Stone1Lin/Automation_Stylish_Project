#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import allure
import logging
import os
import json
from deepdiff import DeepDiff
from Stylish_Project.page_objects.login_page import Login
from Stylish_Project.page_objects.prime_page import PrimePage
from Stylish_Project.api_objects.order_api import OrderAPI, GetOrderAPI
from Stylish_Project.api_objects.user_api import LoginAPI
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.test_data.data_process import DataProcess

file_path = f"Stylish-Test Case.xlsx"
data_process = DataProcess(file_path)
db = DBTable()


@allure.feature("Checkout API")
@allure.story("Checkout with successfully.")
@allure.title(f"Checkout API response within valid value and get order id")
@pytest.mark.parametrize("test_data", data_process.excel_read(f"API Checkout with Valid Value"))
@pytest.mark.OrderAPI
def test_checkout_order_success(session, driver, test_data):
    login = Login(driver)
    prime_page = PrimePage(driver)
    logging.info(test_data)

    with allure.step("Login account."):
        login.login(os.getenv("login_email"), os.getenv("login_pw"))

    with allure.step("Go to prime page."):
        driver.get("http://54.201.140.239/get_prime.html")

    with allure.step("Get prime key."):
        prime_key = prime_page.get_prime(test_data)
        test_data['prime'] = prime_key

    with allure.step("Send OrderAPI request."):
        LoginAPI(session).get_login_info()
        resp = OrderAPI(session).send(test_data)
        assert resp.status_code == 200, f"resp_status_code: {resp.status_code}"


@allure.feature("Checkout order API")
@allure.story("Checkout order failure.")
@allure.title(f"Checkout API response within invalid value and get correct response and error message")
@pytest.mark.parametrize("test_data", data_process.excel_read(f"API Checkout with Invalid Value"))
@pytest.mark.OrderAPI
def test_checkout_order_failure(session, driver, test_data):
    login = Login(driver)
    prime_page = PrimePage(driver)
    logging.info(test_data)

    with allure.step("Login account."):
        login.login(os.getenv("login_email"), os.getenv("login_pw"))

    with allure.step("Go to prime page."):
        driver.get("http://54.201.140.239/get_prime.html")

    with allure.step("Get prime key."):
        prime_key = prime_page.get_prime(test_data)
        test_data['prime'] = prime_key

    with allure.step("Send OrderAPI invalid value."):
        LoginAPI(session).get_login_info()
        resp = OrderAPI(session).send(test_data)

    with allure.step("Verify Http_status_code is correct."):
        assert resp.status_code == int(test_data['Http_status_code']), \
            f"Expected: {int(test_data['Http_status_code'])}, Actual:{resp.status_code}"

    with allure.step("Verify error message is correct."):
        assert resp.json()['errorMsg'] == test_data['Alert Msg'], \
            f"Expected: {test_data['Alert Msg']}, Actual: {resp.json()['errorMsg']}"


@allure.feature("Get Order API")
@allure.story("Get Order with successfully.")
@allure.title(f"Get Order API response within valid value and compare with DB result.")
@pytest.mark.parametrize("test_data", data_process.excel_read(f"API Get Order with valid value"))
@pytest.mark.OrderAPI
def test_get_order_success(session, test_data):
    logging.info(test_data)

    with allure.step("Login account."):
        LoginAPI(session).get_login_info()

    with allure.step("Get order response by order id."):
        resp = GetOrderAPI(session).send(test_data['order_number'])

    with allure.step("Verify Http_status_code is correct."):
        assert resp.status_code == int(test_data['Http_status_code']), \
            f"resp.status_code: {resp.status_code}"

    with allure.step("Compare API data is equal to DB result."):
        db_result = db.get_order_info_by_order_number(test_data['order_number'])
        db_result[0]['details'] = json.loads(db_result[0]['details'])
        db_result[0]['total'] = int(db_result[0]['total'])
        diff = DeepDiff(resp.json()['data'], db_result[0])
        assert diff == {}, f"diff_result: {diff}"


@allure.feature("Get Order API")
@allure.story("Get Order with failure.")
@allure.title(f"Get Order API response within invalid value and get correct response and error message.")
@pytest.mark.parametrize("test_data", data_process.excel_read(f"API GetOrder with invalid value"))
@pytest.mark.OrderAPI
def test_get_order_failure(session, test_data):
    logging.info(test_data)

    with allure.step("Login account."):
        if test_data['Token'] == "True":
            LoginAPI(session).get_login_info()

    with allure.step("Get order response by order id."):
        resp = GetOrderAPI(session).send(test_data['order_number'])

    with allure.step("Verify Http_status_code is correct."):
        assert resp.status_code == int(test_data['Http_status_code']), \
            f"resp.status_code: {resp.status_code}"

    with allure.step("Verify error message is correct."):
        if resp.status_code == 404:
            assert resp.text.strip() == test_data['error msg'], \
                f"Expected: {test_data['error msg']}, Actual: {resp.text.strip()}"
        else:
            assert resp.json()['errorMsg'] == test_data['error msg'], \
                f"Expected: {test_data['error msg']}, Actual: {resp.text}"
