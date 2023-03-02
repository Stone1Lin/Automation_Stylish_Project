#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import allure
from copy import deepcopy
from Stylish_Project.table_object.dbUtils import DBUtils


class DBTable(DBUtils):
    def __init__(self):
        super().__init__()
        self.image_url = "http://54.201.140.239/assets/"

    @allure.step("Execute all product SQL query")
    def all_products_query(self):
        sql_cmd = f"SELECT * FROM stylish_backend.product;"
        return self.execute_select(sql_cmd)

    def get_user_info_by_id(self, user_id):
        sql_cmd = f"SELECT * FROM stylish_backend.user where id={user_id}"
        return self.execute_select(sql_cmd)

    def product_search_by_keyword(self, keyword):
        sql_cmd = f"SELECT * FROM stylish_backend.product WHERE title like '%{keyword}%'"
        return self.execute_select(sql_cmd)

    def product_search_by_prod_id(self, prod_id):
        sql_cmd = f"SELECT * FROM stylish_backend.product WHERE id={prod_id}"
        return self.execute_select(sql_cmd)

    def product_search_by_category(self, category):
        if category == "all":
            sql_cmd = f"SELECT * FROM stylish_backend.product"
        else:
            sql_cmd = f"SELECT * FROM stylish_backend.product WHERE category='{category}'"
        return self.execute_select(sql_cmd)

    def variant_search_by_prod_id(self, prod_id):
        sql_cmd = f"SELECT * \
                    FROM stylish_backend.variant v \
                    INNER JOIN stylish_backend.color c ON v.color_id=c.id \
                    where product_id={prod_id}"

        return self.execute_select(sql_cmd)

    def image_search_by_prod_id(self, prod_id):
        sql_cmd = f"SELECT product_id, image \
                  FROM stylish_backend.product_images WHERE product_id={prod_id}"
        return self.execute_select(sql_cmd)

    def get_order_info_by_order_number(self, order_num):
        sql_cmd = f"SELECT * FROM stylish_backend.order_table where number='{order_num}'"
        return self.execute_select(sql_cmd)

    def get_info_by_keyword(self, keyword):
        prod_result = self.product_search_by_keyword(keyword)
        return self.collect_prod_info(prod_result)

    def get_info_by_prod_id(self, prod_id):
        prod_result = self.product_search_by_prod_id(prod_id)
        return self.collect_prod_info(prod_result)

    def get_info_by_category(self, category):
        prod_result = self.product_search_by_category(category)
        return self.collect_prod_info(prod_result)

    def collect_prod_info(self, prod_result):
        new_prod_info = {}
        for result in prod_result:
            prod_id = result['id']
            main_name = result['main_image']
            result['main_image'] = f"http://54.201.140.239/assets/{prod_id}/{main_name}"
            # Add image URL
            image_result = self.image_search_by_prod_id(prod_id)
            if "images" not in prod_result:
                result["images"] = list()
            for image in image_result:
                images_name = image['image']
                image_url = f"http://54.201.140.239/assets/{prod_id}/{images_name}"
                result["images"].append(image_url)
                variant_result = self.variant_search_by_prod_id(prod_id)
                if "variants" not in prod_result:
                    result["variants"] = list()
                if "colors" not in prod_result:
                    result["colors"] = list()
                if "sizes" not in prod_result:
                    result["sizes"] = list()
                var_dic = {}
                color_dic = {}
                for dic in variant_result:
                    var_dic['color_code'] = dic['code']
                    var_dic['size'] = dic['size']
                    var_dic['stock'] = dic['stock']
                    new_dict = deepcopy(var_dic)
                    result["variants"].append(new_dict)
                    color_dic['code'] = dic['code']
                    color_dic['name'] = dic['name']
                    new_color_dic = deepcopy(color_dic)
                    if new_color_dic not in result["colors"]:
                        result["colors"].append(new_color_dic)
                    if dic['size'] not in result["sizes"]:
                        result["sizes"].append(dic['size'])
        new_prod_info["data"] = prod_result
        return new_prod_info

