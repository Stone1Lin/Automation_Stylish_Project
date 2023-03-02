#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import allure
import logging
import random
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.page_objects.home_page import HomePage
from Stylish_Project.page_objects.product_page import ProductPage


@allure.feature("Product Page Testing")
@allure.story("select a color of the product")
@allure.title("Color Selection")
@pytest.mark.product
def test_color_select(driver):
    """
    Scenario: Color Selection
    Given entered a product page
    When select a color of the product
    Then selected color is highlighted
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a color."):
        random_color = product_page.select_color()
        logging.info(f'Random select color is:{random_color.get_attribute("data_id")}')

    with allure.step("Check the selected color is highlight."):
        selected_color = product_page.selected_color()
        logging.info(f'Highlight color is:{selected_color.get_attribute("data_id")}')

    with allure.step("Verify random color is equal to highlight color."):
        assert random_color.get_attribute("data_id") == selected_color.get_attribute("data_id"),\
            f'random_color: {random_color.get_attribute("data_id")}, ' \
            f'selected_color: {selected_color.get_attribute("data_id")}'


@allure.feature("Product Page Testing")
@allure.story("select a size of the product")
@allure.title("Size Selection")
@pytest.mark.product
def test_size_select(driver):
    """
    Scenario: Size Selection
    Given entered a product page
    When select a size of the product
    Then selected size is highlighted
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a size."):
        random_size = product_page.select_size()
        logging.info(f'Random select size is:{random_size.text}')

    with allure.step("Check the selected size is highlight."):
        selected_size = product_page.selected_size()
        logging.info(f'Highlight size is:{selected_size.text}')

    with allure.step("Verify random size is equal to highlight size."):
        assert random_size.text == selected_size.text,\
            f'random_size: {random_size.text}, selected_size:{selected_size.text}'


@allure.feature("Product Page Testing")
@allure.story("Edit quantity without size selection")
@allure.title("Quantity Editor Disabled")
@pytest.mark.product
def test_quantity_disable(driver):
    """
    Scenario: Quantity Editor Disabled
    Given entered a product page
    When edit quantity without size selection
    Then quantity editor is disabled
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a color."):
        product_page.select_color()

    with allure.step("Get current quantity value."):
        value = product_page.get_quantity_value()
        logging.info(f'Current quantity value:{value}')

    with allure.step("Add one quantity."):
        product_page.add_quantity()

    with allure.step("Get current quantity value after click add one quantity."):
        add_value = product_page.get_quantity_value()
        logging.info(f'Current quantity value:{add_value}')

    with allure.step("Get current quantity on cart button."):
        content = product_page.add_cart_btn()
        logging.info(f'Get current quantity on cart button:{content}')

    with allure.step("Verify value not change without size selection."):
        assert value == add_value, f"default_val: {value}, current_value:{add_value}"

    with allure.step("Verify cart button info is correct."):
        assert content.text == "請選擇尺寸", f"Cart button msg: {content.text}"


@allure.feature("Product Page Testing")
@allure.story("Add quantity and verify quantity value.")
@allure.title("Quantity Editor - Increase Quantity.")
@pytest.mark.product
def test_add_quantity(driver):
    """
    Scenario: Quantity Editor - Increase Quantity
    Given entered a product page
    And  select a size of the product
    When add 8 more quantity
    Then quantity should be 9
    When add 2 more quantity
    Then quantity still be 9
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a color."):
        random_color = product_page.select_color()
        logging.info(f'Random color is:{random_color.get_attribute("data_id")}')

    with allure.step("Check the selected size is highlight."):
        random_size = product_page.select_size()
        logging.info(f'Random size is:{random_size.text}')

    with allure.step("Add 8 more quantity."):
        for i in range(1, 9):
            product_page.add_quantity()
        with allure.step("Verify quantity is 9."):
            assert int(product_page.get_quantity_value()) == 9,\
                f'Current quantity: {int(product_page.get_quantity_value())}'

    with allure.step("Add 2 more quantity."):
        for i in range(1, 3):
            product_page.add_quantity()

        with allure.step("Verify maximize quantity is 9."):
            assert int(product_page.get_quantity_value()) == 9,\
                f'Current quantity: {int(product_page.get_quantity_value())}'


@allure.feature("Product Page Testing")
@allure.story("Select a size of the product and add 8 more quantity")
@allure.title("Quantity Editor - Decrease Quantity.")
@pytest.mark.product
def test_decrease_quantity(driver):
    """
    Scenario: Quantity Editor - Decrease Quantity
    Given entered a product page
    And select a size of the product
    And add 8 more quantity
    When decrease 8 quantity
    Then quantity should be 1
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a color."):
        random_color = product_page.select_color()
        logging.info(f'Random color is:{random_color.get_attribute("data_id")}')

    with allure.step("Check the selected size is highlight."):
        random_size = product_page.select_size()
        logging.info(f'Random size is:{random_size.text}')

    with allure.step("Add 8 more quantity."):
        for i in range(1, 9):
            product_page.add_quantity()
        with allure.step("Verify quantity is 9."):
            assert int(product_page.get_quantity_value()) == 9

    with allure.step("Minus 8 more quantity."):
        for i in range(1, 9):
            product_page.minus_quantity()
        with allure.step("Verify quantity is 1."):
            assert int(product_page.get_quantity_value()) == 1


@allure.feature("Product Page Testing")
@allure.story("Given entered a product page and select a size of the product")
@allure.title("Add To Cart - Success.")
@pytest.mark.product
def test_add_cart(driver):
    """
    Scenario: Add To Cart - Success
    Given entered a product page
    And select a size of the product
    When click add to cart button
    Then success message should be shown
    And cart icon number should be 1
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a color."):
        random_color = product_page.select_color()
        logging.info(f'Random color is:{random_color.get_attribute("data_id")}')

    with allure.step("Check the selected size is highlight."):
        random_size = product_page.select_size()
        logging.info(f'Random size is:{random_size.text}')

    with allure.step("Click add to cart button."):
        product_page.scroll_to_prod_title()
        product_page.add_cart_btn().click()

    with allure.step("Alert should pop up."):
        alert_text = product_page.alert_accept()
        logging.info(f'Alert message: {alert_text}')

    with allure.step("Verify alert message should correct."):
        assert alert_text == '已加入購物車', f'Current msg: {alert_text}'

    with allure.step("Verify cart icon number should be 1."):
        assert int(product_page.get_cart_num()) == 1


@allure.feature("Product Page Testing")
@allure.story("Given entered a product page without size selection")
@allure.title("Add To Cart - Failed.")
@pytest.mark.product
def test_fail_add_cart(driver):
    """
    Scenario: Add To Cart - Failed
    Given entered a product page without size selection
    When click add to cart button
    Then alert message should be shown
    """
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = DBTable().all_products_query()
        product = random.choice(sorted(list(sql_result[i]['title'] for i in range(len(sql_result)))))
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()

    with allure.step("Random select a color."):
        product_page.select_color()

    with allure.step("Random select a color."):
        product_page.add_cart_btn().click()

    with allure.step("Random select a color."):
        alert_text = product_page.alert_accept()
        logging.info(f'Alert message: {alert_text}')

    with allure.step("Verify alert message is '請選擇尺寸'."):
        assert alert_text == '請選擇尺寸', f'Current msg: {alert_text}'

    with allure.step("Verify cart icon number should be 0."):
        assert int(product_page.get_cart_num()) == 0
