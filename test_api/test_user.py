#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import allure
import pytest
import logging
from Stylish_Project.api_objects.user_api import LoginAPI, LogoutAPI, ProfileAPI
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.test_data.data_process import DataProcess
from dotenv import load_dotenv, find_dotenv

load_dotenv(".env")
load_dotenv(find_dotenv())

file_path = f"Stylish-Test Case.xlsx"
data_process = DataProcess(file_path)
db = DBTable()


@allure.feature("User API")
@allure.story("Checkout login successfully.")
@allure.title("Login success and expected result should be correct.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Login with Valid Value'))
@pytest.mark.UserAPI
def test_login_success(test_data, session):
    with allure.step(f"Login with valid value."):
        resp = LoginAPI(session)._send(test_data)

    with allure.step(f"Verify http_status code is success."):
        assert resp.status_code == int(test_data['Http_status_code'])
        assert "data" in resp.json().keys()

    with allure.step(f"Check user info is correctly within DB result."):
        user_id = resp.json()['data']['user']['id']
        db_data = db.get_user_info_by_id(user_id)
        assert resp.json()['data']['access_token'] == db_data[0]['access_token']
        assert int(resp.json()['data']['access_expired']) == db_data[0]['access_expired'], \
            f"{resp.json()['data']['access_expired']}, {db_data[0]['access_expired']}"
        assert resp.json()['data']['user']['provider'] == db_data[0]['provider']
        assert resp.json()['data']['user']['name'] == db_data[0]['name']
        assert resp.json()['data']['user']['email'] == db_data[0]['email']
        assert resp.json()['data']['user']['picture'] == db_data[0]['picture']


@allure.feature("User API")
@allure.story("Checkout login failure.")
@allure.title("Alert message and expected result should be correct.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Login with Invalid Value'))
@pytest.mark.UserAPI
def test_login_failure(test_data, session):
    with allure.step(f"Login with invalid value. -> test_data:{test_data}"):
        resp = LoginAPI(session)._send(test_data)

    with allure.step(f"Verify http_status code is as expected."):
        assert resp.status_code == int(test_data['Http_status_code']), \
            f"Expected: {int(test_data['Http_status_code'])}, Actual: {resp.status_code}"

    with allure.step(f"Verify error message is {test_data['Error msg']}."):
        assert str(resp.json()['errorMsg']) == test_data['Error msg'], \
            f"Expected: {test_data['Error msg']}, Actual: {resp.json()['errorMsg']}"


@allure.feature("User API")
@allure.story("Checkout logout successfully.")
@allure.title("Logout success and expected result should be correct.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Logout with Valid token'))
@pytest.mark.UserAPI
def test_logout_success(test_data, session):
    with allure.step(f"Login account first and get access token."):
        if test_data['Token'] == "valid token":
            access_token, user_id = LoginAPI(session).get_login_info()

    with allure.step(f"Logout successful and verify http_status_code is expected."):
        resp = LogoutAPI(session)._send()
        assert resp.status_code == int(test_data['Http_status_code'])

    with allure.step(f"Verify message is correct."):
        db_data = DBTable().get_user_info_by_id(user_id)
        assert resp.json()['message'] == test_data['message'], \
            f"API response: {resp.json()['message']}, test_data: {test_data['message']}"

    with allure.step(f"Verify access_token is delete from database."):
        assert db_data[0]['access_token'] == "", \
            f"Expected: '', Actual: {db_data[0]['access_token']}"


@allure.feature("User API")
@allure.story("Checkout logout behavior.")
@allure.title("Logout failed and expected result should be correct.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Logout with Invalid token'))
@pytest.mark.UserAPI
def test_logout_failure(test_data, session):
    with allure.step(f"Set access token."):
        if test_data['Token'] == "":
            access_token = ""
        else:
            access_token = test_data['Token']
        LoginAPI(session).set_login_auth(access_token)
        logging.info(f"{session.headers}")
        
    with allure.step(f"Logout with Invalid token."):
        resp = LogoutAPI(session)._send()

    with allure.step(f"Verify status code and error message as expected."):
        assert resp.status_code == int(test_data['Http_status_code'])
        assert resp.json()['errorMsg'] == test_data['message'], \
            f"API response: {resp.json()['errorMsg']}, test_data: {test_data['message']}"


@allure.feature("User API")
@allure.story("Get user profile successfully.")
@allure.title("Get profile success and expected result should be correct.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Profile with Valid Value'))
@pytest.mark.UserAPI
def test_get_user_profile_success(test_data, session):
    with allure.step(f"Login account first and get access token."):
        access_token, user_id = LoginAPI(session).get_login_info()

    with allure.step(f"Get user profile."):
        resp = ProfileAPI(session)._send()

    with allure.step(f"Get profile successful and verify http_status_code is expected."):
        assert resp.status_code == int(test_data['Http_status_code'])

    with allure.step(f"Verify user profile is equal DB result."):
        db_data = DBTable().get_user_info_by_id(user_id)
        assert resp.json()['data']['provider'] == db_data[0]['provider'], \
            f"API: {resp.json()['data']['provider']}, DB: {db_data[0]['provider']}"
        assert resp.json()['data']['name'] == db_data[0]['name'], \
            f"API: {resp.json()['data']['name']}, DB: {db_data[0]['name']}"
        assert resp.json()['data']['email'] == db_data[0]['email'], \
            f"API: {resp.json()['data']['email']}, DB: {db_data[0]['email']}"
        assert resp.json()['data']['picture'] == db_data[0]['picture'], \
            f"API: {resp.json()['data']['picture']}, DB: {db_data[0]['picture']}"


@allure.feature("User API")
@allure.story("Get user profile failure.")
@allure.title("Get profile failed and expected result should be correct.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Profile with Invalid Value'))
@pytest.mark.UserAPI
def test_get_user_profile_failure(test_data, session):
    with allure.step(f"Set access token."):
        if test_data['Token'] == "":
            access_token = ""
        else:
            access_token = test_data['Token']
        LoginAPI(session).set_login_auth(access_token)

    with allure.step(f"Get user profile."):
        resp = ProfileAPI(session)._send()

    with allure.step(f"Get profile failed and verify http_status_code is expected."):
        assert resp.status_code == int(test_data['Http_status_code'])

    with allure.step(f"Verify status code and error message as expected."):
        assert resp.json()['errorMsg'] == test_data['message'], \
            f"API response: {resp.json()['errorMsg']}, test_data: {test_data['message']}"