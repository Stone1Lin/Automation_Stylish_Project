#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import allure
import logging
from Stylish_Project.page_objects.home_page import HomePage
from Stylish_Project.table_object.db_table import DBTable


test_data = ["women", "men", "accessories"]


@allure.story("Product Category Selection")
@allure.title(f"Ensure Category result is fitting: {test_data}")
@pytest.mark.parametrize("category", test_data)
@pytest.mark.category
def test_category_selection(driver, category):
    """
    Scenario: Category Selection (3 Test Cases)
    When select a category (Women / Men / Accessories)
    Then correct products in category should be displayed.

    1. connect to DB get category and store in list
    2. Create .env to store DB connection info
    3. use browser to query and get all items
    4. Ensure all result is fitting.
    """
    homepage = HomePage(driver)
    db_table = DBTable()

    with allure.step("Get SQL query result."):
        sql_result = db_table.product_search_by_category(category)
        logging.info(f'SQL Result: {sql_result}')

    with allure.step("Get web query result."):
        all_products = list(product.text for product in homepage.get_category(category))
        logging.info(f'Web Result: {all_products}')

    with allure.step("Compare data length & data set."):
        db_result_title = sorted(list(sql_result[i]['title'] for i in range(len(sql_result))))
        assert len(db_result_title) == len(all_products)
        assert sorted(all_products) == sorted(db_result_title), \
            f"all product: {all_products}, SQL_result:{db_result_title}"
