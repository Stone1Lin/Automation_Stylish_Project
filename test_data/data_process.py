#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from Stylish_Project.page_objects.excelUtils import ExcelUtils
import os


class DataProcess(ExcelUtils):
    def __init__(self, file_path):
        self.BASE_DIR = os.path.dirname(__file__)
        self.file_path = self.BASE_DIR + f"/{file_path}"
        super().__init__(self.file_path)

    def translate_chars(self, dic_data: dict):
        for i in dic_data:
            for key in i.keys():
                if 'chars' in i[key]:
                    i[key] = int(i[key].replace('chars', ''))*'x'
        return dic_data

    def excel_read(self, sheet_name=""):
        src_data = self.read_excel(sheet_name).to_dict('records')
        test_data = self.translate_chars(src_data)
        return test_data

    def checkout_invalid_data(self, sheet_name="Checkout with Invalid Value"):
        src_data = self.read_excel(sheet_name).to_dict('records')
        test_data = self.translate_chars(src_data)
        return test_data

    def checkout_valid_data(self, sheet_name=""):
        return self.read_excel(sheet_name).to_dict('records')

    def create_product_success(self, sheet_name="Create Product Success"):
        src_data = self.read_excel(sheet_name).to_dict('records')
        test_data = self.translate_chars(src_data)
        return test_data

    def create_product_failed(self, sheet_name="Create Product Failed"):
        src_data = self.read_excel(sheet_name).to_dict('records')
        test_data = self.translate_chars(src_data)
        return test_data
