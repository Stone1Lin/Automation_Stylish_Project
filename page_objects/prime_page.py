#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By
from Stylish_Project.page_objects.base import BasePage


class PrimePage(BasePage):
    CARD_NUMBER = (By.ID, 'cc-number')
    CARD_EXPIRE = (By.ID, 'cc-exp')
    CARD_CVC = (By.ID, 'cc-cvc')
    GET_PRIME_BTN = (By.ID, 'checkoutBtn')
    CARD_NUMBER_IFRAME = (By.XPATH, "//div[@id='card-number']/iframe")
    CARD_EXPIRE_IFRAME = (By.XPATH, "//div[@id='card-expiration-date']/iframe")
    CARD_CVC_IFRAME = (By.XPATH, "//div[@id='card-ccv']/iframe")

    def __init__(self, driver):
        super().__init__(driver)

    def card_number(self):
        return self.find_present_ele(self.CARD_NUMBER)

    def card_expire(self):
        return self.find_present_ele(self.CARD_EXPIRE)

    def card_cvc(self):
        return self.find_present_ele(self.CARD_CVC)

    def get_prime_btn(self):
        return self.find_clickable_ele(self.GET_PRIME_BTN)

    def get_prime(self, data):
        self.switch_to_iframe(self.CARD_NUMBER_IFRAME)
        self.card_number().send_keys(data['Credit Card No'])
        self.switch_to_default_content()

        self.switch_to_iframe(self.CARD_NUMBER_IFRAME)
        self.card_expire().send_keys(data['Expiry Date'])
        self.switch_to_default_content()

        self.switch_to_iframe(self.CARD_CVC_IFRAME)
        self.card_cvc().send_keys(data['Security Code'])
        self.switch_to_default_content()

        self.get_prime_btn().click()
        alert_msg = self.alert_accept()
        return alert_msg
