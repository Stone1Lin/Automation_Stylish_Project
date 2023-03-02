#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import allure
import logging
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.page_objects.home_page import HomePage
from Stylish_Project.page_objects.product_page import ProductPage
from Stylish_Project.page_objects.shopping_cart_page import ShoppingCart
import random


@allure.feature("Shopping Cart")
@allure.story("select a color of the product")
@allure.title("Shopping Cart Info Correct")
@pytest.mark.shopping
def test_shopping_cart_info(driver):
    """
    Scenario: Shopping Cart Info Correct
    When add product to shopping cart
    Then cart info is displayed correctly
    """
    product_page = ProductPage(driver)
    home_page = HomePage(driver)
    db_table = DBTable()

    with allure.step("Random select a product."):
        sql_result = db_table.all_products_query()
        all_products = list(sql_result[i]['title'] for i in range(len(sql_result)))
        logging.info(f"all_products: {all_products}")
        product = random.choice(all_products)
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()
        product_page.select_color()
        product_page.select_size()

    with allure.step("Add product to shopping cart."):
        product_page.add_cart_btn().click()

    with allure.step("Verify alert msg and cart info is displayed correctly."):
        alert_text = product_page.alert_accept()
        cart_quantity = product_page.get_cart_num()
        assert alert_text == '已加入購物車', f"alert_text:{alert_text}"
        assert int(cart_quantity) == 1


@allure.feature("Shopping Cart")
@allure.story("Remove product from cart.")
@allure.title("Cart icon number should be updated correctly")
@pytest.mark.shopping
def test_cart_info_by_remove(driver):
    """
    Given add 2 products to shopping cart
    When delete product from shopping cart
    Then alert message "已刪除商品" should be shown
    And new cart info should be updated correctly
    And cart icon number should be updated correctly
    """
    home = HomePage(driver)
    product_page = ProductPage(driver)
    shopcart_page = ShoppingCart(driver)
    db_table = DBTable()

    with allure.step("Random select two products."):
        sql_result = db_table.all_products_query()
        prod_list = list(sql_result[i]['title'] for i in range(len(sql_result)))
        prod_select = []
        for num in range(2):
            product = random.choice(prod_list)
            home.search_prod(product)
            product_page.click_select_product(product)
            product_page.scroll_to_prod_title()
            product_page.select_color()
            product_page.select_size()
            product_page.add_cart_btn().click()
            alert_text = product_page.alert_accept()
            prod_list.remove(product)
            logging.info(f"product: {product}, cart_info:{alert_text}")
            prod_select.append(product)
        logging.info(f"prod_select: {prod_select}")

    with allure.step("Go to Shopping cart."):
        product_page.shopping_cart_btn().click()

    with allure.step("Random delete a product."):
        del_item = random.choice(prod_select)
        logging.info(f"Delete_prod_name: {del_item}")
        shopcart_page.delete_prod_cart(del_item)

    with allure.step("Verify alert message & cart number is correctly."):
        alert_text = shopcart_page.alert_accept()
        after_del_num = int(product_page.get_cart_num())
        assert alert_text == "已刪除商品"
        assert after_del_num == 1, f"after_del_num:{after_del_num}"


@allure.feature("Shopping Cart")
@allure.story("Edit quantity in cart.")
@allure.title("Subtotal should be updated correctly")
@pytest.mark.shopping
def test_cart_info_correct_after_edit(driver):
    """
    Scenario: Edit quantity in cart
    Given product added to shopping cart
    When edit the quantity of the product
    Then alert message "已修改數量" should be shown
    And subtotal should be updated correctly.
    """
    product_page = ProductPage(driver)
    home_page = HomePage(driver)
    shopcart_page = ShoppingCart(driver)
    db_table = DBTable()

    with allure.step("Random select a product and add qty."):
        qty = random.randint(1, 9)
        sql_result = db_table.all_products_query()
        prod_list = list(sql_result[i]['title'] for i in range(len(sql_result)))
        product = random.choice(prod_list)
        home_page.search_prod(product)
        product_page.click_select_product(product)
        product_page.scroll_to_prod_title()
        product_page.select_color()
        product_page.select_size()
        product_page.add_cart_btn().click()
        product_page.alert_accept()
        product_page.shopping_cart_btn().click()

    with allure.step("Edit the qty of the product."):
        shopcart_page.select_product_qty(product, qty)
        alert_text = shopcart_page.alert_accept()

    with allure.step("Verify the alert message and subtotal are correctly."):
        unit_price = shopcart_page.get_unit_price()
        subtotal = shopcart_page.get_subtotal()
        assert alert_text == "已修改數量", f"alert_text: {alert_text}"
        assert subtotal == unit_price * qty
