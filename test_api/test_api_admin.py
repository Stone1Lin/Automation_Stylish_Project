#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import allure
import logging
from deepdiff import DeepDiff
from Stylish_Project.api_objects.product_api import Prod_DetailAPI
from Stylish_Project.api_objects.admin_api import CreateProductAPI, DeleteProductAPI
from Stylish_Project.api_objects.user_api import LoginAPI
from Stylish_Project.table_object.db_table import DBTable
from Stylish_Project.test_data.data_process import DataProcess

file_path = f"Stylish-Test Case.xlsx"
data_process = DataProcess(file_path)
db = DBTable()


@allure.feature("Admin API")
@allure.story("Create & delete product successfully.")
@allure.title(f"Create & delete product API within valid value and get new product id")
@pytest.mark.parametrize("test_data", data_process.excel_read(f"API Create Product Success"))
@pytest.mark.AdminAPI
def test_create_delete_product_success(session, test_data):
    logging.info(test_data)

    with allure.step("Login account."):
        LoginAPI(session).get_login_info()

    try:
        with allure.step("Create product."):
            resp = CreateProductAPI(session).send(test_data)
            product_id = resp.json()['data']['product_id']

    except Exception as e:
        print(f"Create Product Failed: {test_data['Title']}")

    else:
        with allure.step("Verify the product has add in database."):
            db_result = db.get_info_by_prod_id(product_id)
            assert len(db_result['data']) == 1

        with allure.step("Compare data with API & database query."):
            detail_resp = Prod_DetailAPI(session).send({"Method": "GET", "id": product_id})
            api_result = detail_resp.json()
            diff = DeepDiff(db_result['data'][0], api_result['data'])
            assert diff == {}, f"diff: {diff}"

    finally:
        with allure.step("Check the product existed in database."):
            check_result = db.product_search_by_keyword(test_data['Title'])
            if len(check_result) != 0:
                for product in check_result:
                    prod_id = product['id']
                    with allure.step("Delete created product"):
                        del_resp = DeleteProductAPI(session).send(prod_id)
                        assert del_resp.status_code == 200, f"status_code: {del_resp.status_code}"


@allure.feature("Admin API")
@allure.story("Create product failure.")
@allure.title(f"Create product API within invalid value.")
@pytest.mark.parametrize("test_data", data_process.excel_read(f"API Create Product Failed"))
# @pytest.mark.AdminAPI
def test_create_product_failure(session, test_data):
    logging.info(test_data)

    with allure.step("Login account."):
        LoginAPI(session).get_login_info()

    with allure.step("Create product with invalid value."):
        resp = CreateProductAPI(session).send(test_data)

    with allure.step("Verify http_status_code is expected."):
        assert resp.status_code == int(test_data['Http_Status_code']), \
            f"Expected: {int(test_data['Http_Status_code'])}, Actual: {resp.status_code}"

    with allure.step("Verify error message is expected."):
        assert resp.json()['errorMsg'] == test_data['Error Msg'], \
            f"Expected: {test_data['Error Msg']}, Actual: {resp.json()['errorMsg']}"


@allure.feature("Admin API")
@allure.story("Delete product failure.")
@allure.title(f"Delete product API with invalid value.")
@pytest.mark.parametrize("test_data", data_process.excel_read("API Delete Product Failed"))
# @pytest.mark.AdminAPI
def test_delete_product_failure(session, test_data):
    logging.info(test_data)

    if test_data['Token'] == "valid":
        with allure.step("Login account."):
            LoginAPI(session).get_login_info()

    with allure.step("Delete product with invalid value."):
        resp = DeleteProductAPI(session).send(test_data['product_id'])

    with allure.step("Verify error message is expected."):
        if resp.status_code == 404:
            with allure.step(f"Verify error message is expected if status_code: {resp.status_code}."):
                assert resp.text.strip() == test_data['Error msg']
        else:
            with allure.step(f"Verify error message is expected: {test_data['Error msg']}"):
                assert resp.status_code == int(test_data['Http_status_code'])
                assert resp.json()['errorMsg'] == test_data['Error msg'], \
                    f"Expected: {test_data['Error Msg']}, Actual: {resp.json()['errorMsg']}"
