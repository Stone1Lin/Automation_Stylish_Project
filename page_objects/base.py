# -*- coding: UTF-8 -*-

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_present_ele(self, locator: tuple, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return elem

    def find_clickable_ele(self, locator: tuple, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return elem

    def find_visible_ele(self, locator: tuple, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return elem

    def find_present_eles(self, locator: tuple, timeout=5):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        return elem

    def find_elem_selected(self, locator: tuple, timeout=5):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.element_located_to_be_selected(locator)
        )
        return elem

    def find_all_elems(self, locator: tuple, timeout=5):
        elems = WebDriverWait(self.driver, timeout).until(
            self.driver.find_elements(locator)
        )

        return elems

    def alert_accept(self):
        try:
            msg = WebDriverWait(self.driver, timeout=10).until(
                EC.alert_is_present()
            ).text
            alert = self.driver.switch_to.alert.accept()
            return msg
        except BaseException:
            print("Alert accept error")

    def scroll_page(self, SCROLL_PAUSE_TIME=2):
        Scroll_DelayTime = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return True

    def scroll_to_element(self, elem):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)

    def get_jwt_token(self):
        return self.driver.execute_script('return window.localStorage.getItem("jwtToken");')

    def set_jwt_token(self, token):
        return self.driver.execute_script(f'localStorage.setItem("jwtToken", "{token}");')

    def url_to_be(self, url, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )
        return elem

    def url_match(self, url, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(
            EC.url_matches(url)
        )
        return elem

    def switch_to_iframe(self, locator):
        return self.driver.switch_to.frame(
            self.find_present_ele(locator)
            )

    def switch_to_default_content(self):
        return self.driver.switch_to.default_content()