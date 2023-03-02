#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from Stylish_Project.page_objects.base import BasePage
from selenium.webdriver.common.by import By
from Stylish_Project.table_object.dbUtils import DBUtils


class Login(BasePage):
    PROFILE_LOCATOR = (By.CSS_SELECTOR, ".header__link-icon-profile")
    EMAIL_LOCATOR = (By.CSS_SELECTOR, "#email")
    PASSWORD_LOCATOR = (By.CSS_SELECTOR, "#pw")
    PW_CONFIRM_LOCATOR = (By.CSS_SELECTOR, "#confirm")
    NAME_LOCATOR = (By.CSS_SELECTOR, "#name")
    LOGIN_BTN = (By.XPATH, "//button[text()='Login']")
    LOGOUT_BTN = (By.XPATH, "//div[@class='profile__content']/button")
    SIGN_UP_BTN = (By.XPATH, "//button[text()='Sign Up']")
    SIGN_UP_LINK = (By.XPATH, "//div/a[text()='Sign Up']")

    def __init__(self, driver):
        super().__init__(driver)
        self.__base_url = "http://54.201.140.239/login.html"
        self.driver.get(self.__base_url)

    def enter_email(self, email):
        elem = self.find_present_ele(self.EMAIL_LOCATOR)
        elem.clear()
        elem.send_keys(email)

    def enter_password(self, password):
        elem = self.find_present_ele(self.PASSWORD_LOCATOR)
        elem.clear()
        elem.send_keys(password)

    def click_login_btn(self):
        elem = self.find_present_ele(self.LOGIN_BTN)
        elem.click()

    def click_logout_btn(self):
        elem = self.find_clickable_ele(self.LOGOUT_BTN)
        elem.click()

    def get_db_user_token_by_email(self, email):
        sql_cmd = f"SELECT access_token FROM stylish_backend.user where email='{email}';"
        sql_result = DBUtils().execute_select(sql_cmd)
        token = sql_result[0]['access_token']
        return token

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_btn()
        alert_msg = self.alert_accept()
        return alert_msg
