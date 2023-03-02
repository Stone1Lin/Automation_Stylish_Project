#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
from Stylish_Project.page_objects.base import BasePage
from selenium.webdriver.common.by import By


class ThankYou(BasePage):
    CART_ITEMS = (By.CLASS_NAME, 'cart__item')
    CART_ITEM_NAME = (By.CLASS_NAME, 'cart__item-name')

    def __init__(self, driver):
        super().__init__(driver)

    def get_all_cart_items(self):
        elems = self.find_all_elems(self.CART_ITEM_NAME)
        if len(elems) != 0:
            item_list = []
            for item in elems:
                item_list.append(elems)
        else:
            pass
        return item_list

    # def get_


if __name__ == '__main__':
    from Stylish_Project.page_objects.product_page import ProductPage
    from Stylish_Project.page_objects.login_page import Login
    from Stylish_Project.page_objects.thankyou_page import ThankYou
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    import os
    from dotenv import load_dotenv, find_dotenv
    from Stylish_Project.page_objects.shopping_cart_page import ShoppingCart

    load_dotenv(".env")
    load_dotenv(find_dotenv())


    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())

    login = Login(driver)
    product = ProductPage(driver)
    shopcart = ShoppingCart(driver)
    thankyou = ThankYou(driver)

    login.login(os.getenv("login_email"), os.getenv("login_pw"))
    alert_login = shopcart.alert_accept()

    data = {'Receiver': '陳大文', 'Email': 'abc@abc.com', 'Mobile': '0912345678', 'Address': '台北市', 'Deliver Time': 'Anytime', 'Credit Card No': '4242 4242 4242 4242', 'Expiry Date': '12/69', 'Security Code': '123'}
    prod_list = product.add_product_to_cart(2)
    product.shopping_cart_btn().click()
    logging.info(f"data: {data}")
    shopcart.enter_checkout_info(data)
    shopcart.check_out_btn().click()
    alert_text = shopcart.alert_accept()
    assert alert_text == "付款成功", f"alert_text:{alert_text}"

    ######
    elems = login.find_present_eles(thankyou.CART_ITEM_NAME)
    print(elems)
    if len(elems) != 0:
        item_list = []
        for item in elems:
            item_list.append(elems)
    print(item_list)

    driver.close()
