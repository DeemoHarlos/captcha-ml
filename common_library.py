# -*- coding: utf-8 -*-
import logging
from time import sleep
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s', filename='selenium_log.txt')


class web_element_controller():
    def __init__(self, driver):
        self.driver = driver
        self.current_container = "div.ap-content-wrapper:last-of-type "
        self.current_window = "div.k-window:last-of-type "
        self.drop_down_container = "div.k-animation-container "

    """
    對某個元素進行輸入
    """

    def send_keys(self, css_selector, value):
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, css_selector).send_keys(value)
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

    """
    對某個元素進行點擊
    """

    def click(self, css_selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector).click()
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

    """
    清空某個元素
    """

    def clear(self, css_selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector).clear()
        except Exception as ex:
            logging.error(ex)
        finally:
            pass

    """
    在該頁面上執行javascript
    """

    def run_js(self, js):
        try:
            element = self.driver.execute_script(js)
        except Exception as ex:
            logging.error(ex)
        finally:
            return element

    """
    取得某個元素的html attribute
    """

    def get_attribute(self, css_selector, seq, attr):
        try:
            text = self.driver.execute_script(
                "return $(\""+str(css_selector)+"\")["+str(seq)+"].getAttribute(\""+str(attr)+"\")")
            logging.info("element \"" + str(css_selector) +
                         "\"'s attr " + str(attr) + " is " + str(text))
        except Exception as ex:
            logging.error("return $(\""+str(css_selector) +
                          "\")["+str(seq)+"].getAttribute(\""+str(attr)+"\")")
            logging.error(ex)
        finally:
            return text

    """
    設定某個元素的html attribute
    """

    def set_attribute(self, css_selector, seq, attr, value):
        try:
            text = self.driver.execute_script(
                "return $(\""+str(css_selector)+"\")["+str(seq)+"].setAttribute(\""+attr+"\",\""+value+"\")")
            logging.info("element \"" + str(css_selector) +
                         "\"'s attr " + str(attr) + " is " + text)
        except Exception as ex:
            logging.error(ex)
        finally:
            return text

    """
    取得某個元素的innerHTML
    """

    def get_text(self, css_selector):
        try:
            text = self.driver.execute_script(
                "return $('"+str(css_selector)+"').text().replace( /(\\n|\\r|\\s+) /g,"")")
            logging.info("element \"" + str(css_selector) +
                         "\"'s text is " + text)
        except Exception as ex:
            logging.error(ex)
        finally:
            return text

    """
    設定某個元素的innerHTML
    """

    def set_text(self, css_selector, seq, value):
        try:
            text = self.driver.execute_script(
                "return $(\""+str(css_selector)+"\")["+str(seq)+"].text(\""+value+"\"")
        except Exception as ex:
            logging.error(ex)
        finally:
            return text

    """
    取得某個元素的數量
    """

    def get_length(self, css_selector):
        try:
            text = self.driver.execute_script(
                "return $(\""+str(css_selector)+"\").length")
        except Exception as ex:
            logging.error(ex)
        finally:
            return text

    """
    檢查某個元素是否存在
    """

    def check_exists(self, css_selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except Exception as ex:
            return False
        return True

    """
    當要等待頁面某個元素載入完成時使用
    """

    def wait_element(self, selector, timeout):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("element \"" + selector + "\" found")
        except Exception as ex:
            print(ex)
            logging.error(ex)
        finally:
            return element

    """
    當要等待讀取消失時使用
    """

    def wait_kendo_loading(self, timeout):
        try:
            current_time = 0
            while self.get_length("div.k-loading-image") > 0:
                sleep(0.5)
                current_time += 0.5
                if current_time >= timeout:
                    raise Exception(ES.time_out())
            sleep(1)
        except Exception as ex:
            print(ex)
            logging.error(ex)
        finally:
            return 1

    """
    等待預覽視窗時使用
    """

    def wait_preview_iframe(self, timeout):
        try:
            frame = self.driver.find_element(
                By.CSS_SELECTOR, 'iframe#previewIFrame')
            self.driver.switch_to.frame(frame)
            self.driver.wait_element(
                By.CSS_SELECTOR, '#ActivityImg')
            current_time = 0
            while self.get_attribute("#ActivityImg", 0, "src") == self.get_attribute("#ActivityImg", 0, "data-default-src"):
                sleep(0.5)
                current_time += 0.5
                if current_time >= timeout:
                    raise Exception(ES.time_out())
            self.driver.switch_to.default_content()
        except Exception as ex:
            print(ex)
            logging.error(ex)
        finally:
            return 1

    """
    當要等待兩個元素其一時使用
    """

    def wait_one_of_two_element(self, selector1, selector2, timeout):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                lambda driver: EC.presence_of_element_located((By.CSS_SELECTOR, selector1)) or EC.presence_of_element_located((By.CSS_SELECTOR, selector2)))
            logging.info("element found")
        except Exception as ex:
            print(ex)
            logging.error(ex)
        finally:
            return element

    def test(self, test_str, expectstr):
        if test_str != expectstr:
            raise Exception(ES.unexpected_string())
        return True

    """
    等待某元素直到字串相同
    (isequal為True或是False，為False時，等待某元素直到字串不同)
    """

    def wait_element_until_text_equal(self, css_selector, expect_text, isequal, timeout):
        try:
            element = self.wait_element(css_selector, 10)
            current_text = self.get_text(css_selector)
            current_time = 0
            if isequal:
                while current_text != expect_text:
                    logging.info(current_text + "+" + expect_text)
                    sleep(0.5)
                    current_time += 0.5
                    current_text = self.get_text(css_selector)
                    if current_time >= timeout:
                        raise Exception(ES.time_out())
            else:
                while current_text == expect_text:
                    logging.info(current_text + "+" + expect_text)
                    sleep(0.5)
                    current_time += 0.5
                    current_text = self.get_text(css_selector)
                    if current_time >= timeout:
                        raise Exception(ES.time_out())
            logging.info("element found")
        except Exception as ex:
            print(ex)
            logging.error(ex)
        finally:
            return element

    """
    判斷視窗內是否有404或是500
    """

    def check_for_error_message(self):
        element = self.wait_one_of_two_element(
            ".k-selectable tbody tr", ".k-widget.k-window.k-dialog.ttc-error", 10)
        sleep(1.5)
        grid_errors = self.driver.execute_script(
            "return $(\".k-widget.k-window.k-dialog.ttc-error\").length")
        grid_error_message = self.driver.execute_script(
            "return $(\"#resultMsg\").text()")
        if grid_errors > 0:
            raise Exception(
                str(ES.not_found_or_internal_server_error()) + grid_error_message)
        else:
            logging.info("Page Load Successfully without error.")

    """
    判斷視窗內title是否相符、grid內是否有資料
    """

    def check_for_content(self, title):
        self.wait_kendo_loading(20)
        if self.get_text(self.current_container + ".page-title") != title:
            raise Exception(ES.wrong_authority_or_not_login())
        if self.get_length(self.current_container + ".k-selectable tbody tr") <= 0:
            raise Exception(ES.page_no_data_or_initialize_error())

    """
    點選視窗內Kendo下拉選單的第index個值
    """

    def click_kendo_drop_down_list(self, aria_owns, index):
        try:
            self.run_js(
                "$(\"" + self.current_window + "span[aria-owns="+aria_owns+"]\").click()")
            sleep(2)
            self.run_js(
                "$(\"" + self.drop_down_container + "ul#"+aria_owns+" li\")["+str(index)+"].click()")
        except Exception as ex:
            logging.error("$(\"" + self.current_window +
                          "span[aria-owns="+aria_owns+"]\").click()")
            logging.error("$(\"" + self.drop_down_container +
                          "ul#"+aria_owns+" li\")["+str(index)+"].click()")
            logging.error(ex)

    def select_element(self, css_selector, value):
        try:
            element = Select(self.driver.find_element(By.CSS_SELECTOR))
            element.select_by_value(value)
            return element
        except Exception as ex:
            logging.error(ex)

    """
    在富文本編輯器內輸入文字
    """

    def type_in_kendo_richtextbox(self, attribute, text):
        element = self.driver.find_element(By.CSS_SELECTOR, self.current_window +
                                           "label[for="+attribute+"]")
        element = element.find_element(By.XPATH, "..")
        frame = element.find_element(
            By.CSS_SELECTOR, 'iframe.k-content')
        self.driver.switch_to.frame(frame)
        editable = self.driver.find_element(By.CSS_SELECTOR, 'html body')
        editable.send_keys(text)
        self.driver.switch_to.default_content()

    """
    在numerictextbox裡面輸入文字
    """

    def type_in_kendo_numerictextbox(self, attribute, value):
        element = self.driver.find_element(By.CSS_SELECTOR, self.current_window +
                                           "input[name="+attribute+"]")
        element = element.find_element(By.XPATH, "../..")
        element = element.find_element(By.CSS_SELECTOR, ".k-link-increase")
        for x in range(0, int(value)):
            element.click()

    """
    點擊切頁
    """

    def swap_page(self, data_page_url):
        self.run_js(
            "$(\".nav__list li[data-page-url='"+data_page_url+"']\").click()")

    """
    確認對話
    """

    def confirm_dialog(self):
        self.wait_kendo_loading(10)
        self.click(self.current_window+".window-footer .k-button.k-primary")
        self.wait_kendo_loading(10)
        self.click(self.current_window +
                   "div[role=toolbar] .k-button:first-child")
        self.wait_kendo_loading(10)
        self.wait_element(self.current_window, 20)
        self.click(self.current_window +
                   "div[role=toolbar] .k-button:first-child")
        self.wait_kendo_loading(10)

    """
    關閉最上層的window
    """

    def close_window(self):
        try:
            self.click(self.current_window+"a[aria-label=\"Close\"]")
        except Exception as ex:
            raise Exception(ES.not_found_or_internal_server_error())
    """
    填入表單
    """

    def fill_form(self, is_in_window, data_object):
        window_prefix = self.current_window if is_in_window else ""
        for attribute, data_row in data_object.items():
            input_type = data_row["input_type"]
            value = data_row["value"]
            logging.info(str(attribute) + " " +
                         str(input_type) + " " + str(value))
            if input_type == "input" or input_type == "textarea":
                css_selector = window_prefix + \
                    input_type + "[name="+str(attribute)+"]"
                if self.get_attribute(css_selector, 0, "value") != "":
                    self.clear(css_selector)
                self.send_keys(css_selector, value)
            elif input_type == "rich_textbox":
                self.type_in_kendo_richtextbox(attribute, value)
            elif input_type == "numeric_box":
                self.type_in_kendo_numerictextbox(attribute, value)
            elif input_type == "dropdownlist":
                self.click_kendo_drop_down_list(attribute, value)
            elif input_type == "checkbox_list":
                for check_attr, is_check in value.items():
                    logging.info(str(check_attr) + " " +
                                 str(is_check))
                    if is_check:
                        self.click(window_prefix+"input#"+str(check_attr))
            elif input_type == "selections":
                logging.info(self.current_window +
                             "button[data-bind=\"click: "+attribute+"\"]")
                self.click(
                    self.current_window + "button[data-bind=\"click: "+attribute+"\"]")
                self.wait_kendo_loading(10)
                self.run_js(
                    "$(\""+self.current_window + "tbody tr td label\")["+str(value)+"].click()")
                self.click(self.current_window +
                           ".window-footer .k-button.k-primary")
                for x in range(0, data_row["maximum"]):
                    self.click(self.current_window +
                               "div.couponItem .k-link-increase")
