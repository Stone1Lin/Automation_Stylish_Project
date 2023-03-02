#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import allure
import logging
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.page_objects.home_page import HomePage
from Stylish_Project.page_objects.product_page import ProductPage
from Stylish_Project.page_objects.login_page import Login
from Stylish_Project.page_objects.shopping_cart_page import ShoppingCart
from Stylish_Project.test_data.data_process import DataProcess
import os
import random

file_path = f"Stylish-Test Case.xlsx"
data_process = DataProcess(file_path)


@allure.feature("Checkout")
@allure.story("Checkout with empty cart.")
@allure.title("Alert message should be shown correctly.")
@pytest.mark.checkout
def test_checkout_empty_qty(driver):
    """
    [condition] Should be login success
    Scenario: Checkout with empty cart
    When click checkout button without add product to shopping cart
    Then alert message "尚未選購商品" should be shown
    """
    shopcart_page = ShoppingCart(driver)
    product_page = ProductPage(driver)

    with allure.step("Login account."):
        login = Login(driver)
        login.login(os.getenv("login_email"), os.getenv("login_pw"))
        shopcart_page.alert_accept()

    with allure.step("Click shopping cart button."):
        product_page.shopping_cart_btn().click()
        shopcart_page.scroll_page()

    with allure.step("Check out and verify alert message."):
        shopcart_page.check_out_btn().click()
        alert_msg = shopcart_page.alert_accept()
        assert alert_msg == "尚未選購商品"


@allure.feature("Checkout")
@allure.story("Checkout with invalid value.")
@allure.title("Related alert message should be shown with invalid value.")
@pytest.mark.parametrize("data", data_process.checkout_invalid_data(f"Checkout with Invalid Value"))
@pytest.mark.checkout
def test_checkout_invalid_value(driver, data):
    """
    Scenario: Checkout with invalid values (17 Test Cases)
    Given login success
    And add product to shopping cart
    When checkout with invalid value (According to Stylish-Test Case.xlsx - \
    Checkout with Invalid Value" sheet)
    Then related alert message should be shown
    """
    login = Login(driver)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    shopcart_page = ShoppingCart(driver)
    db_table = DBTable()

    with allure.step("Login account."):
        login.login(os.getenv("login_email"), os.getenv("login_pw"))
        login.alert_accept()

    with allure.step("Random select a product and go to checkout page."):
        sql_result = db_table.all_products_query()
        all_products = list(sql_result[i]['title'] for i in range(len(sql_result)))
        product = random.choice(all_products)
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()
        product_page.select_color()
        product_page.select_size()
        product_page.add_cart_btn().click()
        product_page.alert_accept()
        product_page.shopping_cart_btn().click()
        logging.info(f"product: {product}")

    with allure.step("Fillup the checkout info."):
        shopcart_page.enter_checkout_info(data)
        shopcart_page.check_out_btn().click()
    with allure.step("Verify alert message is correctly."):
        alert_text = shopcart_page.alert_accept()
        assert alert_text == data['Alert Msg'], f"alert_text:{alert_text}"


@allure.feature("Checkout")
@allure.story("Checkout with valid values.")
@allure.title(f"Alert message 付款成功 should be shown with valid value.")
@pytest.mark.parametrize("data", data_process.checkout_invalid_data(f"Checkout with Valid Value"))
@pytest.mark.checkout
def test_checkout_valid_value(driver, data):
    """
    Scenario: Checkout with valid values (3 Test Cases)
    Given login success
    And add product to shopping cart
    When checkout with valid value (According to Stylish-Test Case.xlsx - "Checkout with Valid Value" sheet)
    Then alert message "付款成功" should be shown
    And correct order info should be displayed in thankyou page
    """

    login = Login(driver)
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    shopcart_page = ShoppingCart(driver)
    db_table = DBTable()

    with allure.step("Login account."):
        login.login(os.getenv("login_email"), os.getenv("login_pw"))
        login.alert_accept()

    with allure.step("Random select a product and go to checkout page."):
        sql_result = db_table.all_products_query()
        all_products = list(sql_result[i]['title'] for i in range(len(sql_result)))
        product = random.choice(all_products)
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()
        product_page.select_color()
        product_page.select_size()
        product_page.add_cart_btn().click()
        product_page.alert_accept()
        product_page.shopping_cart_btn().click()
        logging.info(f"product: {product}")

    with allure.step("Fillup the checkout info."):
        shopcart_page.enter_checkout_info(data)
        shopcart_page.check_out_btn().click()

    with allure.step("Verify alert message '付款成功' should be shown"):
        alert_text = shopcart_page.alert_accept()
        assert alert_text == "付款成功", f"alert_text:{alert_text}"

