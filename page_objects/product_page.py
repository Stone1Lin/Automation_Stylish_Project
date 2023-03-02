#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import allure
from Stylish_Project.page_objects.base import BasePage
from selenium.webdriver.common.by import By
import random


class ProductPage(BasePage):
    PROD_TITLE = (By.CSS_SELECTOR, '.product__title')
    SIZE_LOCATOR = (By.XPATH, '//div[@class="product__size-selector"]/child::*')
    COLOR_LOCATOR = (By.XPATH, '//div[@class="product__color-selector"]/child::*')
    SELECTED_SIZE_LOCATOR = (By.CSS_SELECTOR, 'div[class*="product__size--selected"]')
    SELECTED_COLOR_LOCATOR = (By.CSS_SELECTOR, 'div[class*="product__color--selected"]')
    SELECTED_PRODUCTS = (By.XPATH, '//div[@class="products"]/child::*')
    QUANTITY_LOCATOR = (By.XPATH, '//div[@class="product__quantity-selector"]/child::*')
    QUANTITY_ADD = (By.CSS_SELECTOR, '.product__quantity-add')
    QUANTITY_MINUS = (By.CSS_SELECTOR, '.product__quantity-minus')
    QUANTITY_VALUE = (By.CSS_SELECTOR, '.product__quantity-value')
    CART_BTN = (By.CSS_SELECTOR, '.product__add-to-cart-button')
    CART_NUM = (By.CSS_SELECTOR, '.header__link-icon-cart-number')
    SHOPPING_CART = (By.CSS_SELECTOR, '.header__link-icon-cart')

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Get color elements")
    def select_color(self):
        elem = random.choice(self.find_present_eles(self.COLOR_LOCATOR))
        elem.click()
        return elem

    @allure.step("Get select color")
    def selected_color(self):
        return self.find_present_ele(self.SELECTED_COLOR_LOCATOR)

    @allure.step("Get products element")
    def products_select(self):
        return random.choice(self.find_present_eles(self.SELECTED_PRODUCTS))

    @allure.step("Get size elements")
    def select_size(self):
        elem = random.choice(self.find_present_eles(self.SIZE_LOCATOR))
        elem.click()
        return elem

    @allure.step("Get select size")
    def selected_size(self):
        elem = self.find_present_ele(self.SELECTED_SIZE_LOCATOR)
        elem.click()
        return elem

    @allure.step("Get add quantity element and click")
    def add_quantity(self):
        elem = self.find_present_ele(self.QUANTITY_ADD)
        elem.click()
        return elem

    @allure.step("Get minus quantity element and click")
    def minus_quantity(self):
        elem = self.find_present_ele(self.QUANTITY_MINUS)
        elem.click()
        return elem

    @allure.step("Get quantity value")
    def get_quantity_value(self):
        elem = self.find_present_ele(self.QUANTITY_VALUE)
        logging.info(f"Get Quantity Num: {elem.text}")
        return elem.text

    @allure.step("Get add cart btn element")
    def add_cart_btn(self):
        return self.find_present_ele(self.CART_BTN)

    @allure.step("Get shopping cart btn element")
    def shopping_cart_btn(self):
        return self.find_present_ele(self.SHOPPING_CART)

    @allure.step("Get cart number element")
    def get_cart_num(self):
        elem = self.find_present_ele(self.CART_NUM)
        logging.info(f"Get Cart Num: {elem.text}")
        return elem.text

    @allure.step("Scroll to product title on product page")
    def scroll_to_prod_title(self):
        self.scroll_to_element(self.find_present_ele(self.PROD_TITLE))

    @allure.step("Get random product")
    def get_random_prod(self, prod_list):
        return random.choice(prod_list)

    @allure.step("Click select product")
    def click_select_product(self, prod_name):
        elem = self.find_present_ele(
            (By.XPATH, f"//div[@class='product__title' and contains(text(), '{prod_name}')]")
        ).click()
        return elem

