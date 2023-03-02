#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from Stylish_Project.api_objects.base_api import BaseAPI


class CreateProductAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/admin/product"
        # self.BASE_DIR = os.path.abspath(os.path.dirname(os.getcwd()))
        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    def send(self, test_data):
        payload = {
            "category": test_data['Category'],
            "title": test_data['Title'],
            "description": test_data['Description'],
            "price": test_data['Price'],
            "texture": test_data['Texture'],
            "wash": test_data['Wash'],
            "place": test_data['Place of Product'],
            "note": test_data['Note'],
            "story": test_data['Story'],
            "color_ids": test_data['ColorIDs'].split(','),
            "sizes": test_data['Sizes'].split(',')
        }
        files = []
        if test_data["Main Image"] == 'sample image':
            main_image = ('main_image', open(
                f'{self.BASE_DIR}/test_data/mainImage.jpeg', 'rb'))
            files.append(main_image)
        if test_data["Other Image 1"] == 'sample image':
            other_images0 = ('other_images', open(
                f'{self.BASE_DIR}/test_data/otherImage0.jpg', 'rb'))
            files.append(other_images0)
        if test_data["Other Image 2"] == 'sample image':
            other_images1 = ('other_images', open(
                f'{self.BASE_DIR}/test_data/otherImage1.jpg', 'rb'))
            files.append(other_images1)

        return self.request('post', url=self.url, data=payload, files=files)


class DeleteProductAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session)
        self.url = "http://54.201.140.239/api/1.0/admin/product/"

    def send(self, product_id):
        return self.request("delete", url=f"{self.url}{product_id}")
