#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import allure
import logging
import os
from Stylish_Project.page_objects.login_page import Login
from dotenv import load_dotenv, find_dotenv

load_dotenv(".env")
load_dotenv(find_dotenv())


@allure.feature("Login Testing")
@allure.story("JWT token behavior in local storage and database.")
@allure.title("Login and Logout Success.")
@pytest.mark.login
def test_login_success(driver, email=os.getenv("login_email"), password=os.getenv("login_pw")):
    """
    Scenario: Login and Logout Success
    When member login with correct email and password
    Then login success and there is jwt token in local storage
    When member logout
    Then logout success
    """
    login = Login(driver)
    with allure.step("Login with correct email and password"):
        login.enter_email(email)
        login.enter_password(password)
        login.click_login_btn()

    with allure.step("Check alert message while login success."):
        alert_msg = login.alert_accept()
        assert alert_msg == "Login Success", f"alert_msg:{alert_msg}"

    with allure.step("JWT token should stored in localStorage and equal to access_token in database."):
        jwtToken = login.get_jwt_token()
        db_token = login.get_db_user_token_by_email(email)
        logging.info(f"Login success: jwtToken:{jwtToken}, db_token:{db_token}")
        assert jwtToken is not None, f"JWT token:{jwtToken}"
        assert jwtToken == db_token, f"jwtToken:{jwtToken}, db_token:{db_token}"

    with allure.step("Check alert message and JWT token deleted after log out."):
        login.click_logout_btn()
        logout_msg = login.alert_accept()
        jwt_token = login.get_jwt_token()
        db_token = login.get_db_user_token_by_email(email)
        logging.info(f"Logout success: jwtToken:{jwt_token}, db_token:{db_token}")
        assert logout_msg == "Logout Success", f"logout_msg: {logout_msg}"
        assert jwt_token is None and db_token == "", f"JWT token:{jwt_token}, db_token:{db_token}"


@allure.feature("Login Testing")
@allure.story("Login Failed with incorrect email or password")
@allure.title("Login failure with invalid email & password.")
@pytest.mark.parametrize("email, password", [
    ("", os.getenv("login_pw")),
    (os.getenv("login_email"), ""),
    ("abc@test.com", os.getenv("login_pw")),
    (os.getenv("login_email"), "abcdefg")])
@pytest.mark.login
def test_login_fail(driver, email, password):
    """
    Scenario: Login Failed with incorrect email or password
    When member login with incorrect email / password
    Then login failed with error message
    """
    login = Login(driver)
    with allure.step("Login Failed with incorrect email or password."):
        logging.info(f"email:{email}, password:{password}")
        login.enter_email(email)
        login.enter_password(password)
        login.click_login_btn()
        login_msg = login.alert_accept()

    with allure.step("Verify login failed with error message."):
        if email == "" or password == "":
            assert login_msg == "Email and password are required.", f"email:{email}, password:{password}"
        else:
            assert login_msg == "Login Failed"


@allure.feature("Access Authorization")
@allure.story("Using invalid access token to visit profile page.")
@allure.title("Login with invalid access token.")
@pytest.mark.login
def test_login_with_invalid_access_token(driver, email=os.getenv("login_email"), password=os.getenv("login_pw")):
    """
    Scenario: Login with invalid access token
    Given member login with correct email and password
    And login success and copy the jwt token
    And member logout
    And logout success
    When using the jwt token to access member page
    Then error message "Invalid Token"
    """
    login = Login(driver)
    with allure.step("Login with correct email and password"):
        login.enter_email(email)
        login.enter_password(password)
        login.click_login_btn()

    with allure.step("Login success and copy the jwt token"):
        alert_msg = login.alert_accept()
        jwtToken = login.get_jwt_token()
        logging.info(f"Login success - jwtToken:{jwtToken}")
        assert alert_msg == "Login Success", f"alert_msg:{alert_msg}"

    with allure.step("logout success and set jwt token in local storage"):
        login.click_logout_btn()
        login.alert_accept()
        set_token = login.set_jwt_token(jwtToken)

    with allure.step("Using the jwt token to visit profile page."):
        driver.get("http://54.201.140.239/profile.html")

    with allure.step("Verify alert message is correct."):
        invalid_alert = login.alert_accept()
        assert invalid_alert == "Invalid Access Token"

    with allure.step("Redirect to Login page"):
        assert login.url_to_be("http://54.201.140.239/login.html") is True

