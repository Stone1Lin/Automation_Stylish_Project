#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import allure
import logging
from Stylish_Project.page_objects.base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class HomePage(BasePage):
    SEARCH_FIELD = (By.CSS_SELECTOR, '.header__search-input')
    SEARCH_RESULT = (By.XPATH, '//div[@class="products"]/child::a')
    PRODUCT_TITLE = (By.CSS_SELECTOR, '.product__title')

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Search product by product name.")
    def search_prod(self, prod_name=""):
        search_field = self.find_present_ele(self.SEARCH_FIELD)
        actions = ActionChains(self.driver)
        actions.send_keys_to_element(search_field, prod_name)
        actions.send_keys_to_element(search_field, Keys.ENTER)
        actions.perform()
        self.scroll_page()

    @allure.step("Get product search results.")
    def get_search_result(self, prod_name=""):
        self.search_prod(prod_name)
        self.scroll_page()
        try:
            if not self.find_present_eles(self.SEARCH_RESULT):
                pass
            else:
                search_result = self.find_present_eles(self.PRODUCT_TITLE)
                return search_result
        except Exception as e:
            return []

    @allure.step("Get product category.")
    def get_category(self, category):
        category = category.lower()
        self.find_present_ele((By.XPATH, f'//div/a[@href="./index.html?category={category}"]')).click()
        self.scroll_page()
        all_products = self.find_present_eles(self.PRODUCT_TITLE)
        return all_products

