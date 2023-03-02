#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random

import allure
import logging
from Stylish_Project.page_objects.base import BasePage
from Stylish_Project.page_objects.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep


class ShoppingCart(BasePage):
    FIELD_RECEIVER = (By.XPATH, "//div[contains(text(), '收件人姓名')]/following-sibling::input")
    FIELD_EMAIL = (By.XPATH, "//div[contains(text(), 'Email')]/following-sibling::input")
    FIELD_MOBILE = (By.XPATH, "//div[contains(text(), '手機')]/following-sibling::input")
    FIELD_ADDRESS = (By.XPATH, "//div[contains(text(), '地址')]/following-sibling::input")
    DELIVER_TIMES = (By.CSS_SELECTOR, ".form__field-name")
    CREDITCARD_NUM = (By.ID, 'cc-number')
    CREDITCARD_EXP = (By.ID, 'cc-exp')
    CREDITCARD_CCV = (By.ID, 'cc-ccv')
    CREDITCARD_NUM_IFRAME = (By.XPATH, "//div[@id='card-number']/iframe")
    CREDITCARD_EXP_IFRAME = (By.XPATH, "//div[@id='card-expiration-date']/iframe")
    CREDITCARD_CCV_IFRAME = (By.XPATH, "//*[@id='card-ccv']/iframe")
    CART_ITEMS = (By.CSS_SELECTOR, '.cart__items')
    CART_NUM = (By.CSS_SELECTOR, '.header__link-icon-cart-number')
    UNIT_PRICE = (By.CLASS_NAME, 'cart__item-price-content')
    SUBTOTAL = (By.XPATH, "//div[@class='total']/div[@class='total__amount']")
    TOTAL = (By.XPATH, "//div[@class='payable']/div[@class='total__amount']")
    FREIGHT = (By.XPATH, "//div[@class='freight']/div[@class='total__amount']")
    CHECK_OUT_BTN = (By.CSS_SELECTOR, '.checkout-button')

    def __init__(self, driver):
        super().__init__(driver)

    def cart_delete_locator(self, prod_name):
        return f"//div[text()='{prod_name}']/parent::div[@class='cart__item-detail']/following-sibling::div[4]"

    def cart_qty_locator(self, prod_name):
        return f"//div[text()='{prod_name}']/parent::div[@class='cart__item-detail']/following-sibling::div[1]/select"

    def get_unit_price(self):
        elem = self.find_present_ele(self.UNIT_PRICE).text
        return int(elem.strip("NT."))

    def get_subtotal(self):
        elem = self.find_present_ele(self.SUBTOTAL).text
        return int(elem.strip("NT."))

    def product_qty(self, prod_name):
        elem = self.find_present_ele(
            (By.XPATH, f"{self.cart_qty_locator(prod_name)}")
        )
        return elem

    def check_out_btn(self):
        return self.find_present_ele(self.CHECK_OUT_BTN)

    def select_product_qty(self, prod_name, qty):
        qty_elem = self.product_qty(prod_name)
        select = Select(qty_elem)
        select.select_by_visible_text(str(qty))
        logging.info(f"select: {select}")

    def delete_prod_cart(self, prod_name):
        elem = self.find_present_ele(
            (By.XPATH, f"{self.cart_delete_locator(prod_name)}")
        ).click()
        return elem

    def receiver_name(self):
        return self.find_present_ele(self.FIELD_RECEIVER)

    def email(self):
        return self.find_present_ele(self.FIELD_EMAIL)

    def mobile(self):
        return self.find_present_ele(self.FIELD_MOBILE)

    def address(self):
        return self.find_present_ele(self.FIELD_ADDRESS)

    @allure.step("Scroll to deliver time on shop cart page.")
    def scroll_to_deliver_time(self):
        elem = self.find_present_ele(self.DELIVER_TIMES)
        self.scroll_to_element(elem)

    def select_deliver_time(self, time_range):
        if time_range != "":
            deliver_time = {
                "Morning": 1,
                "Afternoon": 2,
                "Anytime": 3
            }
            index = deliver_time[time_range]
            elem = self.find_present_ele((By.XPATH, f"//*[@class='form__field-radios']/child::label[{index}]"))
            elem.click()

    def credit_card_num(self):
        return self.find_present_ele(self.CREDITCARD_NUM)

    def credit_card_exp(self):
        return self.find_present_ele(self.CREDITCARD_EXP)

    def credit_card_ccv(self):
        return self.find_present_ele(self.CREDITCARD_CCV)

    def enter_checkout_info(self, data):
        self.scroll_to_deliver_time()
        self.receiver_name().send_keys(data['Receiver'])
        self.email().send_keys(data['Email'])
        self.mobile().send_keys(data['Mobile'])
        self.address().send_keys(data['Address'])
        self.select_deliver_time(data['Deliver Time'])

        self.switch_to_iframe(self.CREDITCARD_NUM_IFRAME)
        self.credit_card_num().send_keys(data['Credit Card No'])
        self.switch_to_default_content()

        self.switch_to_iframe(self.CREDITCARD_EXP_IFRAME)
        self.credit_card_exp().send_keys(data['Expiry Date'])
        self.switch_to_default_content()

        self.scroll_page()
        self.switch_to_iframe(self.CREDITCARD_CCV_IFRAME)
        self.credit_card_ccv().send_keys(data['Security Code'])
        self.switch_to_default_content()