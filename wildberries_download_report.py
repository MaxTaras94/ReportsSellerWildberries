# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:20:23 2022

@author: taras
"""
from config import (phone_number, wb_url, url_report_3, url_report_4, url_report_11, dir_for_save_reports)
from datetime import datetime
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time



class DownloadReportWildberries:
    '''
        Класс для скачивания отчёта из лк продавца Wildberries
    '''
    def __init__(self):
        self.__chrome_options = Options()
        self.__chrome_options.add_argument("--headless")
        self.__chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.4.863 Yowser/2.5 Safari/537.36")
        self.__chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": dir_for_save_reports, # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        self.__chrome_options.experimental_options["prefs"] = prefs
        self.browser = webdriver.Chrome("chromedriver.exe", options=self.__chrome_options)
        
    def start(self):
        self._login()
        self. download_report_sales()
        self.download_report_brand_share()
        self.download_report_warehouse_remains()
        print("Выгрузка отчётов закончена")
        
    def _login(self, auth_cookies=True) -> bool:
        """Функция для входа в лк продавца Wildberries"""
        self.browser.get(wb_url)
        print("Авторизация на сайте")
        if auth_cookies:
            for cookie in pickle.load(open("cook_wild", "rb")):
                self.browser.add_cookie(cookie)
            self.browser.refresh()
            print("Авторизация прошла успешно")
            return True
        else:
            try:
                phone_num = self.browser.find_element(By.TAG_NAME,  value="input")
                phone_num.send_keys(phone_number)
                butt_get_code = self.browser.find_element(By.CLASS_NAME, value="Login-phone__button--AvFeU")
                butt_get_code.click()
                self.save_cookies()
                return True
            except:
                return False
            
    def save_cookies(self):
        """Функция сохраняет куки текущей сессии в папку с проектом"""
        pickle.dump(self.browser.get_cookies(), open("cook_wild", "wb"))
        
    def download_report_sales(self, date_from=datetime.today().strftime('%d.%m.%Y'), date_to=datetime.today().strftime('%d.%m.%Y')):
        """Функция выгружает отчет по продажам из лк продавца Wildberries"""
        self.browser.get(url_report_3)
        print("Выгружаю отчет по продажам")
        try:
            self.browser.find_element(By.CLASS_NAME, value="WarningCookiesBannerCard__button__E6TkOOyxzr").click() # попытка кликнуть на кнопку Принять куки
        except NoSuchElementException:
            pass
        self.browser.find_element(By.CLASS_NAME, value="Date-input__icon-button__CPx0Ca4N2z").click()
        time.sleep(0.3)
        if not date_from:
            try:
                self.browser.find_elements(By.CLASS_NAME, value="Simple-input__Ua-RpiriLS")[1].find_element(By.TAG_NAME, value="input").send_keys(date_from) # ввод даты начала периода формирования отчета
                time.sleep(0.5)
                self.browser.find_elements(By.CLASS_NAME, value="Simple-input__Ua-RpiriLS")[-1].find_element(By.TAG_NAME, value="input").send_keys(date_from) # ввод даты начала периода формирования отчета
                time.sleep(0.5)
                self.browser.find_element(By.CLASS_NAME, value="DatePickerMenu__save-button__RNh8SIN-35").click() # нажатие на кнопку сохранить выбранную дату
            except NoSuchElementException:
                return "Не удалось указать дату для выгрузки отчёта"
            time.sleep(1)
            try:
                self.browser.find_element(By.CLASS_NAME, value="WarningCookiesBannerCard__button__E6TkOOyxzr").click() # попытка кликнуть на кнопку Принять куки
            except NoSuchElementException:
                pass
            topics_xpath = "//div[@class='Export-button__Gij5Q2THSr']//span[text()='Выгрузить в Excel']"
            elem = self.browser.find_element(By.XPATH, value=topics_xpath)
            time.sleep(1)
            elem.click() # нажатие на кнопку Выгрузить в Excel
        
        
    def download_report_brand_share(self):
        """Функция выгружает отчет по долям брендов в продажах из лк продавца Wildberries"""
        print("Выгружаю отчет по долям брендов в продажах")
        self.browser.get(url_report_4)

    def download_report_warehouse_remains(self):
        """Функция выгружает отчет по остаткам на складе из лк продавца Wildberries"""
        self.browser.get(url_report_11)
        print("Выгружаю отчет по остаткам на складе")
        topics_xpath = "//button[@class='Button-link__YPcDbilyau Button-link--button__M-0nTjDTHF Button-link--interface__vnZbVDTowf Button-link--button-big__z3J9T2QnNl']//span[text()='Выгрузить в Excel']"
        elem = self.browser.find_element(By.XPATH, value=topics_xpath)
        time.sleep(1)
        elem.click() # нажатие на кнопку Выгрузить в Excel

chrome_options = Options()
chrome_options.add_argument("--headless=chrome")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.4.863 Yowser/2.5 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
prefs = {'download.default_directory' : dir_for_save_reports}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome("chromedriver.exe", options=chrome_options)
browser.get(wb_url)
for cookie in pickle.load(open("cook_wild", "rb")):
    browser.add_cookie(cookie)
browser.refresh()
browser.get(url_report_3)
time.sleep(1)

browser.find_element(By.CLASS_NAME, value="Date-input__icon-button__CPx0Ca4N2z").click()
time.sleep(1.5)
browser.find_elements(By.CLASS_NAME, value="Simple-input__Ua-RpiriLS")[1].find_element(By.TAG_NAME, value="input").send_keys(date_from) # ввод даты начала периода формирования отчета
time.sleep(1)
browser.find_elements(By.CLASS_NAME, value="Simple-input__Ua-RpiriLS")[-1].find_element(By.TAG_NAME, value="input").send_keys(date_from) # ввод даты начала периода формирования отчета
time.sleep(1)
browser.find_element(By.CLASS_NAME, value="DatePickerMenu__save-button__RNh8SIN-35").click() # нажатие на кнопку сохранить выбранную дату
time.sleep(1)
try:
    browser.find_element(By.CLASS_NAME, value="WarningCookiesBannerCard__button__E6TkOOyxzr").click() # попытка кликнуть на кнопку Принять куки
except NoSuchElementException:
    pass
topics_xpath = "//div[@class='Export-button__Gij5Q2THSr']//span[text()='Выгрузить в Excel']"
elem = browser.find_element(By.XPATH, value=topics_xpath)
# browser.execute_script("arguments[0].scrollIntoView(true);", elem)
elem.click()
browser.find_element(By.CLASS_NAME, value="Export-button__Gij5Q2THSr").click()
browser.quit()

wb_download_reports = DownloadReportWildberries()

if __name__ == "__main__":
    wb = DownloadReportWildberries()
    wb.start()