#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import os


if __name__ == '__main__':
    pytest.main(['-vs', '--video=on', '--screenshot=on',
                 '--alluredir=./report/xml', '--clean-alluredir'])
    os.system(r"allure generate --clean ./report/xml -o ./report/html")
    os.system(r"allure open ./report/html")