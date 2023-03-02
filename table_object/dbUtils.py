#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pymysql
import allure
import pandas as pd
import os
import logging
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine

load_dotenv(".env")
load_dotenv(find_dotenv())


class DBUtils:
    def __init__(self):
        self.__db_setting = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_DATABASE"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": int(os.getenv("DB_PORT"))
        }

        # self.__conn_info = f'mysql+pymysql://{self.__db_setting["user"]}:{self.__db_setting["password"]}' \
        #                    f'@{self.__db_setting["host"]}:{self.__db_setting["port"]}/{self.__db_setting["database"]}'

    def create_connection(self):
        try:
            db = pymysql.connect(**self.__db_setting)

            # db = create_engine(f"{self.__conn_info}", encoding='utf-8')
            return db
        except Exception as e:
            print(e)
            return None

    def execute_select(self, sql_cmd):
        conn = self.create_connection()
        try:
            df = pd.read_sql(sql_cmd, con=conn)
            # df = pd.read_sql_query(sql=sql_cmd, con=conn)
            sql_result = df.to_dict('records')
            return sql_result
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    from Stylish_Project.table_object.db_table import DBTable

    db = DBTable()
    result = db.get_info_by_keyword("洋裝")
    print(result)
