from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, TimeoutException

WAIT_TIMEOUT = 10


def wait_visibility_by_name(driver: webdriver, name: str):
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            ec.visibility_of_element_located((By.NAME, name))
        )
    except (TimeoutException, NoSuchElementException):
        current_timestamp = datetime.now()
        print(f'[ERROR] {current_timestamp} ---> Name "{name}" is not visible!')


def wait_visibility_by_xpath(driver: webdriver, xpath: str):
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            ec.visibility_of_element_located((By.XPATH, xpath))
        )
    except (TimeoutException, NoSuchElementException):
        current_timestamp = datetime.now()
        print(f'[ERROR] {current_timestamp} ---> XPath "{xpath}" is not visible!')


def wait_invisibility_by_xpath(driver: webdriver, xpath: str):
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            ec.invisibility_of_element_located((By.XPATH, xpath))
        )
    except (TimeoutException, NoSuchElementException):
        current_timestamp = datetime.now()
        print(f'[ERROR] {current_timestamp} ---> XPath "{xpath}" is visible!')


def wait_visibility_by_id(driver: webdriver, target_id: str):
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            ec.visibility_of_element_located((By.ID, target_id))
        )
    except (TimeoutException, NoSuchElementException):
        current_timestamp = datetime.now()
        print(f'[ERROR] {current_timestamp} ---> ID "{target_id}" is not visible!')


def wait_vilibility_by_class_name(driver: webdriver, class_name: str):
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            ec.presence_of_element_located((By.CLASS_NAME, class_name))
        )
    except (TimeoutException, NoSuchElementException):
        current_timestamp = datetime.now()
        print(f'[ERROR] {current_timestamp} ---> Class name "{class_name}" nis not visible!')
