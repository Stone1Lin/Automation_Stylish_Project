#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import allure
import pytest
import os

from Stylish_Project.page_objects.login_page import Login
from Stylish_Project.page_objects.admin_page import Admin
from Stylish_Project.test_data.data_process import DataProcess
from dotenv import load_dotenv, find_dotenv

load_dotenv(".env")
load_dotenv(find_dotenv())

file_path = f"Stylish-Test Case.xlsx"
data_process = DataProcess(file_path)


@allure.feature("Create Product")
@allure.story("Create product with valid values.")
@allure.title("Create Product Success.")
@pytest.mark.parametrize("data", data_process.create_product_success())
@pytest.mark.admin
def test_create_product_success(driver, data):
    """
    Scenario: Create Product Success (3 Test Cases)
    Given login success
    When create product with valid values (According to Stylish-Test Case.xlsx -
        "Create Product Success" sheet)
    Then alert message "Create Product Success" should be shown
    And new product should be displayed on product list
    """
    login_page = Login(driver)
    admin_page = Admin(driver)

    with allure.step("Login account."):
        login_page.login(os.getenv("login_email"), os.getenv("login_pw"))

    with allure.step("Go to admin page"):
        driver.get(os.getenv("admin_prod_create"))

    with allure.step("Input new product infoInput new product info"):
        alert_msg = admin_page.enter_new_product_info(data)

    with allure.step("alert message should be shown and correctly."):
        alert_msg == "Create Product Success"

    with allure.step("New product should be displayed on product list."):
        driver.get(os.getenv("admin_prod_list"))
        assert admin_page.check_new_product_title(data["Title"]) is True

    with allure.step("Delete product from Admin Page."):
        admin_page.delete_product(data["Title"])
        delete_msg = admin_page.alert_accept()
        assert delete_msg == "Delete Product Success", f"delete_msg:{delete_msg}"


@allure.feature("Create Product")
@allure.story("Create Product with Invalid Value(20 Test Cases).")
@allure.title("Create Product Failed.")
@pytest.mark.parametrize("data", data_process.create_product_failed())
@pytest.mark.admin
def test_create_product_failed(driver, data):
    """
    Scenario: Create Product with Invalid Value (20 Test Cases)
    Given login success
    When create product with invalid values (According to Stylish-Test Case.xlsx - "Create Product Failed" sheet)
    Then related alert message should be shown
    """
    login_page = Login(driver)
    admin_page = Admin(driver)
    with allure.step("Login account."):
        login_page.login(os.getenv("login_email"), os.getenv("login_pw"))

    with allure.step("Go to create new product"):
        driver.get("http://54.201.140.239/admin/product_create.html")

    with allure.step("Input new product info"):
        alert_msg = admin_page.enter_new_product_info(data)

    with allure.step("alert message should be shown and correctly."):
        alert_msg == data["Alert Msg"], f'alert_msg: {alert_msg}, expected: {data["Alert Msg"]}'


@allure.feature("Create Product")
@allure.story("Create product with valid values.")
@allure.title("Create Product without login.")
@pytest.mark.parametrize("data", data_process.create_product_success())
@pytest.mark.admin
def test_create_product_without_login(driver, data):
    """
    Scenario: Create Product without login
    When create product with valid values
    Then alert message "Please Login first" should be shown
    And should be redirected to login page
    """
    admin_page = Admin(driver)

    with allure.step("Go to create new product"):
        driver.get("http://54.201.140.239/admin/product_create.html")

    with allure.step("Input new product info"):
        alert_msg = admin_page.enter_new_product_info(data)

    with allure.step("alert message should be shown and correctly."):
        alert_msg == "Please Login first", f"alert_msg:{alert_msg}"



