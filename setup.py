# -*- coding: utf-8 -*-
import logging
import os.path as path
import sys
from inspect import getsourcefile
from selenium.webdriver.common.by import By
import logging
import random
from time import sleep
from selenium import webdriver
import common_library as lib
import urllib.request

"""
Created on Wed Jan 16 17:39:47 2019

@author: andrew_hsu
"""

current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir)


driver = webdriver.Firefox()
driver.get("https://tixcraft.com/ticket/ticket/19_BSB/5407/14/16")
web_element_controller = lib.web_element_controller(driver)
try:
    for i in range(2501,3000):
        web_element_controller.click("#yw0")
        web_element_controller.check_exists("#yw0")
        src = web_element_controller.get_attribute("#yw0",0,"src")
        logging.info(src)
        urllib.request.urlretrieve("https://tixcraft.com" +src, "test_img_new/" + str(i) + ".png")
        sleep(0.1)




except Exception as ex:
    logging.error(ex)
finally:
    sys.path.pop(0)
    sys.path.pop(0)
