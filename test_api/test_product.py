#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import allure
import pytest
from deepdiff import DeepDiff
from Stylish_Project.debug_talk import DebugTalk
from Stylish_Project.api_objects.product_api import Prod_SearchAPI, Prod_DetailAPI, Prod_CategoryAPI
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.test_data.data_process import DataProcess

file_path = f"Stylish-Test Case.xlsx"
data_process = DataProcess(file_path)
db = DBTable()


@allure.feature("Product API")
@allure.story("Search product by keyword successfully.")
@allure.title("Search API response by params within keyword and compare data correction.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Search with valid value'))
@pytest.mark.ProductAPI
def test_product_search_success(session, test_data):
    allure.dynamic.title(test_data['Description'])

    with allure.step(f"Search product -> keyword: {test_data['keyword']}, paging: {test_data['paging']}"):
        resp = Prod_SearchAPI(session).send(test_data)
        # [TODO] Add paging validation.

    with allure.step(f"Verify http_status_code is equal to {int(test_data['Http_status_code'])}."):
        assert resp.status_code == int(test_data['Http_status_code']), \
            f"Expected: {int(test_data['Http_status_code'])}, Actual: {resp.status_code}"

    with allure.step(f"Query database by keyword."):
        api_result = resp.json()
        db_result = db.get_info_by_keyword(test_data['keyword'])

    with allure.step("Compared API & database result."):
        diff = DeepDiff(api_result, db_result)
        assert "data" in resp.json().keys()
        assert len(db_result['data']) == len(api_result['data']), \
            f"db_len: {len(db_result['data'])}, api_len: {len(api_result['data'])}"
        assert diff == {}, f"Diff_result: {diff}"

    with allure.step("If search result not empty, validate image links are available."):
        if len(api_result['data']) != 0:
            for i in range(len(api_result['data'])):
                assert DebugTalk().check_url_exists(api_result['data'][0]['main_image']) is True, \
                    f"main_images: {api_result['data'][0]['main_image']}"
                for link in api_result['data'][0]['images']:
                    assert DebugTalk().check_url_exists(link) is True, f"Image_link: {link}"


@allure.feature("Product API")
@allure.story("Search product by keyword failure.")
@allure.title("Search product with invalid value and verify error message.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Search with invalid value'))
@pytest.mark.ProductAPI
def test_product_search_failure(session, test_data):
    allure.dynamic.title(test_data['Description'])

    with allure.step(f"Search product -> keyword: {test_data['keyword']}, paging: {test_data['paging']}"):
        resp = Prod_SearchAPI(session).send(test_data)

    with allure.step(f"Verify http_status_code is equal to {int(test_data['Http_status_code'])}."):
        assert resp.status_code == int(test_data['Http_status_code']), \
            f"Expected: {int(test_data['Http_status_code'])}, Actual: {resp.status_code}"

    with allure.step(f"Verify error message is expected result: {test_data['message']}"):
        assert resp.json()['errorMsg'] == test_data['message'], \
            f"API response: {resp.json()['errorMsg']}, test_data: {test_data['message']}"


@allure.feature("Product API")
@allure.story("Search product by product ID successfully.")
@allure.title("Details API response by params with valid value.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Detail with valid value'))
@pytest.mark.ProductAPI
def test_product_search_details_success(session, test_data):
    allure.dynamic.title(test_data['Description'])

    with allure.step(f"Search by product_id -> keyword: {test_data['id']}"):
        resp = Prod_DetailAPI(session).send(test_data)
        api_result = resp.json()

    with allure.step(f"Verify http_status_code is equal to {int(test_data['Http_status_code'])}."):
        assert resp.status_code == int(test_data['Http_status_code'])

    with allure.step(f"Query database by product_id."):
        db_result = db.get_info_by_prod_id(test_data['id'])

        with allure.step("Compared API & database result."):
            diff = DeepDiff(api_result['data'], db_result['data'][0])
            assert "data" in api_result.keys()
            assert len(db_result['data']) == len(api_result), \
                f"db_len: {len(db_result['data'])}, api_len: {len(api_result)}"
            assert diff == {}, f"Diff_result: {diff}"


@allure.feature("Product API")
@allure.story("Search product by product ID failure.")
@allure.title("Details API response by params with invalid value.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Detail with invalid value'))
@pytest.mark.ProductAPI
def test_product_search_details_failure(session, test_data):
    allure.dynamic.title(test_data['Description'])

    with allure.step(f"Search by product_id -> keyword: {test_data['id']}"):
        resp = Prod_DetailAPI(session).send(test_data)

    with allure.step(f"Verify http_status_code is equal to {int(test_data['Http_status_code'])}."):
        assert resp.status_code == int(test_data['Http_status_code'])

    with allure.step(f"Verify error message is expected result: {test_data['message']}"):
        assert resp.json()['errorMsg'] == test_data['message'], \
            f"API response: {resp.json()['errorMsg']}, test_data: {test_data['message']}"


@allure.feature("Product API")
@allure.story("Search product by category successfully.")
@allure.title("Category API response by params within valid value.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Category with valid value'))
@pytest.mark.ProductAPI
def test_product_category_success(session, test_data):
    allure.dynamic.title(test_data['Description'])

    with allure.step(f"Search by product category -> category: {test_data['category']}"):
        resp = Prod_CategoryAPI(session).send(test_data)
        assert resp.status_code == int(test_data['Http_status_code'])

    with allure.step(f"Query database by category"):
        api_result = resp.json()
        category_data = resp.json()
        while 'next_paging' in api_result:
            test_data['paging'] = api_result['next_paging']
            resp_nextpage = Prod_CategoryAPI(session).send(test_data)
            api_result = resp_nextpage.json()
            category_data['data'].extend(api_result['data'])
        db_result = db.get_info_by_category(test_data['category'])

    with allure.step(f"Compared API & DB result."):
        diff = DeepDiff(category_data['data'], db_result['data'])
        assert "data" in api_result.keys()

        assert len(db_result['data']) == len(category_data['data']), \
            f"db_len: {len(db_result['data'])}, api_len: {len(category_data['data'])}"
        assert diff == {}, f"Diff_result: {diff}"


@allure.feature("Product API")
@allure.story("Search product by category failure.")
@allure.title("Category API response by params within invalid value.")
@pytest.mark.parametrize("test_data", data_process.excel_read('API Category with invalid value'))
@pytest.mark.ProductAPI
def test_product_category_failure(session, test_data):
    allure.dynamic.title(test_data['Description'])

    with allure.step(f"Search by product category -> category: {test_data['category']}"):
        resp = Prod_CategoryAPI(session).send(test_data)
        assert resp.status_code == int(test_data['Http_status_code'])

        if int(test_data['Http_status_code']) == 404:
            with allure.step(f"Compared API response is equal to expected: {test_data['message']}."):
                assert resp.status_code == int(test_data['Http_status_code'])
                assert resp.text.strip() == test_data['message']

        else:
            with allure.step(f"Compared API response is equal to expected: {test_data['message']}."):
                assert resp.json()['errorMsg'] == test_data['message'], \
                    f"API response: {resp.json()['errorMsg']}, test_data: {test_data['message']}"