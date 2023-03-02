#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import allure
import os
from .base import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class Admin(BasePage):
    CATEGORY = (By.CSS_SELECTOR, 'select[name=category]')
    TITLE = (By.CSS_SELECTOR, 'input[name="title"]')
    DESCRIPTION = (By.CSS_SELECTOR, 'textarea[name="description"]')
    PRICE = (By.CSS_SELECTOR, 'input[name="price"]')
    TEXTURE = (By.CSS_SELECTOR, 'input[name="texture"]')
    WASH = (By.CSS_SELECTOR, 'input[name="wash"]')
    PLACE = (By.CSS_SELECTOR, 'input[name="place"]')
    NOTE = (By.CSS_SELECTOR, 'input[name="note"]')
    STORY = (By.CSS_SELECTOR, 'input[name="story"]')
    MAIN_IMAGE = (By.CSS_SELECTOR, 'input[name="main_image"]')
    OTHER_IMAGES_1 = (By.XPATH, "//input[@name='main_image']/following::input[1]")
    OTHER_IMAGES_2 = (By.XPATH, "//input[@name='main_image']/following::input[2]")
    CREATE_BTN = (By.CSS_SELECTOR, 'input[type="submit"]')
    PRODUCT_TITLE = (By.ID, 'product_title')
    PRODUCT_CATEGORY = (By.ID, 'product_category')

    def __init__(self, driver):
        super().__init__(driver)
        self.BASE_DIR = os.path.dirname(os.getcwd())

    def select_colors(self, colors):
        # [TODO] 可使用 //XPATH , text 方式定位
        colors = colors.replace(" ", "").split(',')
        color = {
            "白色": 1, "亮綠": 2, "淺灰": 3, "淺棕": 4,
            "淺藍": 5, "深藍": 6, "粉紅": 7}
        if "全選" in colors:
            for color_no in range(len(color)):
                self.find_clickable_ele((By.XPATH, f"//input[@id='color_ids' and @value='{color_no+1}']")).click()
        elif "" not in colors:
            for color_no in range(len(colors)):
                self.find_visible_ele((By.XPATH, f"//input[@id='color_ids' and @value='{color_no+1}']")).click()

    def select_sizes(self, sizes):
        sizes = sizes.replace(" ", "").split(',')
        if "全選" in sizes:
            for index in ["S", "M", "L", "XL", "F"]:
                self.find_present_ele((By.XPATH, f"//input[@name='sizes' and @value='{index}']")).click()
        elif "" not in sizes:
            for index in sizes:
                self.find_present_ele((By.XPATH, f"//input[@name='sizes' and @value='{index}']")).click()

    def select_category(self, category):
        category = category.lower()
        option = Select(self.find_present_ele(self.CATEGORY))
        option.select_by_value(f"{category}")

    def input_title(self, title):
        return self.find_present_ele(self.TITLE).send_keys(f"{title}")

    def input_description(self, content):
        return self.find_present_ele(self.DESCRIPTION).send_keys(content)

    def input_price(self, price):
        return self.find_present_ele(self.PRICE).send_keys(price)

    def input_texture(self, texture):
        return self.find_present_ele(self.TEXTURE).send_keys(texture)

    def input_wash(self, wash):
        return self.find_present_ele(self.WASH).send_keys(wash)

    def input_place(self, place):
        return self.find_present_ele(self.PLACE).send_keys(place)

    def input_note(self, note):
        self.find_present_ele(self.NOTE).send_keys(note)
        
    def input_story(self, story):
        return self.find_present_ele(self.STORY).send_keys(story)

    def upload_main_image(self):
        file = self.BASE_DIR + f"/Stylish_Project/test_data/mainImage.jpeg"
        return self.find_present_ele(self.MAIN_IMAGE).send_keys(file)

    def upload_image1(self):
        file = self.BASE_DIR + f"/Stylish_Project/test_data/otherImage0.jpg"
        return self.find_present_ele(self.OTHER_IMAGES_1).send_keys(file)

    def upload_image2(self):
        file = self.BASE_DIR + f"/Stylish_Project/test_data/otherImage1.jpg"
        return self.find_present_ele(self.OTHER_IMAGES_2).send_keys(file)

    def click_create_btn(self):
        return self.find_clickable_ele(self.CREATE_BTN).click()
        
    def enter_new_product_info(self, data):
        self.select_category(data["Category"])
        self.input_title(data["Title"])
        self.input_description(data["Description"])
        self.input_price(data["Price"])
        self.input_texture(data["Texture"])
        self.input_wash(data["Wash"])
        self.input_place(data["Place of Product"])
        self.input_note(data["Note"])
        self.select_colors(data["Colors"])
        self.select_sizes(data["Sizes"])
        self.input_story(data["Story"])
        if data['Main Image'] == "sample image":
            self.upload_main_image()
        if data['Other Image 1'] == "sample image":
            self.upload_image1()
        if data['Other Image 2'] == "sample image":
            self.upload_image2()
        self.click_create_btn()
        alert_msg = self.alert_accept()
        return alert_msg

    def delete_product(self, prod_title):
        return self.find_present_ele(
            (By.XPATH, f"//td[@id='product_title' and text()='{prod_title}']/following::button")).click()

    def check_new_product_title(self, prod_title):
        return self.find_present_ele(
            (By.XPATH, f"//td[@id='product_title' and text()='{prod_title}']")
        ).is_displayed()


