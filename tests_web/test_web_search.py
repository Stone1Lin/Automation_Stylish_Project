#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import allure
import logging
from Stylish_Project.page_objects.home_page import HomePage
from Stylish_Project.table_object.db_table import DBTable

test_data = ["洋裝", "", "Hello"]


@allure.story("Search Product")
@allure.title(f"Test Search Product: {test_data}")
@pytest.mark.parametrize("prod_name", test_data)
@pytest.mark.search
def test_prod_search(driver, prod_name):
    """
    Scenario: Search Product By Keyword
    When search with keyword "洋裝"
    Then all searched product title should be included "洋裝"

    Scenario: Search Product Without Keyword
    When search with empty keyword
    Then all products should be displayed

    Scenario: Search Product - No Product Found
    When search with keyword "Hello"
    Then no product should be displayed
    """
    homepage = HomePage(driver)

    with allure.step("Get SQL query result:"):
        sql_result = DBTable().product_search_by_keyword(prod_name)
        logging.info(f"sql_result: {sql_result}")

    with allure.step("Get web query result."):
        result = homepage.get_search_result(prod_name)
        logging.info(f'Web Result: {sorted(list(product.text for product in result))}')

    with allure.step("Verify result & data set."):
        db_result_title = sorted(list(sql_result[i]['title'] for i in range(len(sql_result))))
        web_result_title = sorted(list(product.text for product in result))
        assert web_result_title == db_result_title, \
            f"Web result: {web_result_title}, DB Result: {db_result_title}"
