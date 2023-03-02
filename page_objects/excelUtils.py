#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pandas as pd


class ExcelUtils:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self, sheet_name=""):
        try:
            excel_df = pd.read_excel(self.file_path, sheet_name=sheet_name, dtype=str)
            data = excel_df.fillna("")
            return data

        except FileNotFoundError:
            raise Exception(f"{self.file_path} is not exist.")

