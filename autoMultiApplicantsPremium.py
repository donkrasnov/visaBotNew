import multiprocessing
import random
import time
from datetime import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, ElementNotVisibleException, \
    ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from twocaptcha import TwoCaptcha

import spainApplicants
import waitByMethods

TEST_URL = 'https://ya.ru'
BLS_SPAIN_URL = 'https://blsspain-russia.com/moscow/book_appointment.php'
YANDEX_URL = 'https://passport.yandex.ru/auth?retpath=https%3A%2F%2Fmail.yandex.ru'
WAIT_TIMEOUT = 10
VISA_TYPE = '11'
NUM_CORE = 4
API_KEY = 'a8c29c48cfc7bd56a2519f4584961fa1'
sitekey_first_captcha = '748d19a1-f537-4b8b-baef-281f70714f56'

option = webdriver.ChromeOptions()
option.add_experimental_option('detach', True)


class textOutputColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fill_first_form(driver: webdriver, category_booking: str, applicant: spainApplicants.Applicant):
    centre = driver.find_element(By.ID, 'centre')
    Select(centre).select_by_value('6#1')
    time.sleep(0.1)

    waitByMethods.wait_visibility_by_xpath(driver, '//option[@value="Normal" and text()="Обычная подача"]')
    category = driver.find_element(By.ID, 'category')
    if category_booking == 'Premium':
        Select(category).select_by_value('Premium')
        waitByMethods.wait_vilibility_by_class_name(driver, 'close')
        red_cross = driver.find_element(By.CLASS_NAME, 'close')
        red_cross.click()
    else:
        Select(category).select_by_value('Normal')

    waitByMethods.wait_visibility_by_id(driver, 'phone')
    phone = driver.find_element(By.ID, 'phone')
    phone.send_keys(applicant.phone)

    email = driver.find_element(By.ID, 'email')
    email.send_keys(applicant.email)

    waitByMethods.wait_visibility_by_id(driver, 'verification_code')
    verification_code_button = driver.find_element(By.ID, 'verification_code')
    verification_code_button.click()


def solve_h_captcha(driver: webdriver, url: str, sitekey, applicant: spainApplicants.Applicant):
    start_time_local = datetime.now()
    solver = TwoCaptcha(API_KEY)
    h_captcha_response_name = 'h-captcha-response'

    current_timestamp = datetime.now()
    print(f'[INFO] {current_timestamp} ---> Solving BLS hCAPTCHA for ---> {applicant.email}')
    key = solver.hcaptcha(sitekey, url)['code']
    end_time_local = datetime.now()
    current_timestamp = datetime.now()
    print(
        f'[INFO] {current_timestamp} ---> BLS hCAPTCHA was solved by: {end_time_local - start_time_local} for ---> {applicant.email}')

    h_captcha_response_input_field = driver.find_element(By.NAME, h_captcha_response_name)
    driver.execute_script(
        "arguments[0].style.display = 'block';", h_captcha_response_input_field
    )
    h_captcha_response_input_field.send_keys(key)


def is_captcha_yandex(driver: webdriver):
    try:
        driver.find_element(By.CLASS_NAME, 'CheckboxCaptcha-Button')
        return True
    except NoSuchElementException:
        try:
            driver.find_element(By.CLASS_NAME, 'AdvancedCaptcha-ImageWrapper')
            return True
        except NoSuchElementException:
            return False


def check_email(driver: webdriver, applicant: spainApplicants.Applicant):
    while is_captcha_yandex(driver):
        current_timestamp = datetime.now()
        print(f"[ACTION] {current_timestamp} ---> Solve YANDEX CAPTCHA for ---> {applicant.email}")
        time.sleep(10)

    waitByMethods.wait_visibility_by_id(driver, 'passp:sign-in')
    try:
        button = driver.find_element(By.CSS_SELECTOR, 'button[data-t="button:clear"][data-type="login"]')
        button.click()
    except NoSuchElementException:
        pass

    waitByMethods.wait_visibility_by_id(driver, 'passp-field-login')
    login_input = driver.find_element(By.ID, 'passp-field-login')
    login_input.send_keys(applicant.login)

    waitByMethods.wait_visibility_by_id(driver, 'passp:sign-in')
    login_button = driver.find_element(By.ID, 'passp:sign-in')
    login_button.click()

    waitByMethods.wait_visibility_by_id(driver, 'passp-field-passwd')
    password_input = driver.find_element(By.ID, 'passp-field-passwd')
    password_input.send_keys(applicant.password)

    waitByMethods.wait_visibility_by_id(driver, 'passp:sign-in')
    login_button = driver.find_element(By.ID, 'passp:sign-in')
    login_button.click()
    time.sleep(2)

    while is_captcha_yandex(driver):
        current_timestamp = datetime.now()
        print(f"[ACTION] {current_timestamp} ---> Solve YANDEX CAPTCHA for ---> {applicant.email}")
        time.sleep(5)

    # waitByMethods.wait_visibility_by_xpath(driver, '//span[text()="OTP Confirmation"]')
    email = driver.find_element(By.XPATH, '//span[text()="OTP Confirmation"]')
    email.click()

    waitByMethods.wait_visibility_by_xpath(driver, '//a[text()="Click here to view your verification code"]')
    link = driver.find_element(By.XPATH, '//a[text()="Click here to view your verification code"]')
    link.click()

    driver.switch_to.window(driver.window_handles[-1])

    waitByMethods.wait_visibility_by_name(driver, 'email')
    input_email = driver.find_element(By.NAME, 'email')
    input_email.send_keys(applicant.email)

    form_element = driver.find_element(By.NAME, 'Submit')
    form_element.click()

    waitByMethods.wait_vilibility_by_class_name(driver, 'blurry-text')
    otp_string = driver.find_element(By.CLASS_NAME, 'blurry-text')
    otp_string = otp_string.text
    otp_last_four = otp_string[-4:]

    current_timestamp = datetime.now()
    print(f"[INFO] {current_timestamp} ---> OTP: {otp_last_four} for ---> {applicant.email}")

    driver.switch_to.window(driver.window_handles[0])
    waitByMethods.wait_vilibility_by_class_name(driver, 'ns-view-toolbar-button-delete')
    delete_email = driver.find_element(By.CLASS_NAME, 'ns-view-toolbar-button-delete')
    delete_email.click()
    driver.quit()

    return otp_last_four


def input_otp_and_continue(driver: webdriver, otp_value: str, applicant: spainApplicants.Applicant):
    waitByMethods.wait_visibility_by_id(driver, 'otp')
    otp_element = driver.find_element(By.ID, 'otp')
    otp_element.send_keys(otp_value)

    solve_h_captcha(driver, BLS_SPAIN_URL, sitekey_first_captcha, applicant)
    # Change if hCAPTCHA can't be solved automatically
    # time.sleep(30)

    waitByMethods.wait_visibility_by_name(driver, 'save')
    continue_button = driver.find_element(By.NAME, 'save')
    continue_button.click()

    waitByMethods.wait_visibility_by_name(driver, 'agree')
    agree_button = driver.find_element(By.NAME, 'agree')
    agree_button.click()


def continue_after_second_form(driver: webdriver, applicant: spainApplicants.Applicant):
    solve_h_captcha(driver, BLS_SPAIN_URL, sitekey_first_captcha, applicant)
    # Change if hCAPTCHA can't be solved automatically
    # time.sleep(30)

    waitByMethods.wait_visibility_by_name(driver, 'save')
    continue_button = driver.find_element(By.NAME, 'save')
    continue_button.click()

    current_timestamp = datetime.now()
    print(f"[INFO] {current_timestamp} ---> Second form filled for ---> {applicant.email}")


def refresh_page_before_bls_captcha_is_working(driver: webdriver, applicant: spainApplicants.Applicant):
    timeout = 60
    starting_time = time.time()

    while time.time() - starting_time < timeout:
        try:
            WebDriverWait(driver, 2).until(ec.visibility_of_element_located(
                (By.XPATH, '//div[@aria-label="Disabled: Account has been suspended"]')))
            current_timestamp = datetime.now()
            print(f"[ERROR] {current_timestamp} ---> CAPTCHA was broken for ---> {applicant.email}")
        except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
            break

    current_timestamp = datetime.now()
    print(f"[INFO] {current_timestamp} ---> BLS hCAPTCHA is working now for ---> {applicant.email}")


def refresh_page_before_element_visible_by_class_name(driver: webdriver, class_name: str,
                                                      applicant: spainApplicants.Applicant):
    # waitByMethods.wait_visibility_by_id(driver, 'app_date')
    # app_date = driver.find_element(By.ID, 'app_date')
    # app_date.click()
    while class_name not in driver.page_source:
        waitByMethods.wait_visibility_by_id(driver, 'app_date')
        app_date = driver.find_element(By.ID, 'app_date')
        app_date.click()
        current_timestamp = datetime.now()
        print(f"[INFO] {current_timestamp} ---> No available date for ---> {applicant.email}")
        time.sleep(30)
        driver.refresh()

    current_timestamp = datetime.now()
    print(f"[INFO] {current_timestamp} ---> Available date found for ---> {applicant.email}")


def fill_second_form(driver: webdriver, applicant: spainApplicants.Applicant):
    waitByMethods.wait_visibility_by_id(driver, 'travelDate')
    travel_date = driver.find_element(By.ID, 'travelDate')
    driver.execute_script(f"arguments[0].setAttribute('value','{applicant.travel_date}')", travel_date)

    waitByMethods.wait_visibility_by_id(driver, 'VisaTypeId')
    visa_type = driver.find_element(By.ID, 'VisaTypeId')
    Select(visa_type).select_by_value(VISA_TYPE)

    waitByMethods.wait_visibility_by_id(driver, 'first_name')
    first_name = driver.find_element(By.ID, 'first_name')
    first_name.send_keys(applicant.first_name)

    waitByMethods.wait_visibility_by_id(driver, 'last_name')
    last_name = driver.find_element(By.ID, 'last_name')
    last_name.send_keys(applicant.last_name)

    waitByMethods.wait_visibility_by_id(driver, 'dateOfBirth')
    birth_date = driver.find_element(By.ID, 'dateOfBirth')
    driver.execute_script(f"arguments[0].setAttribute('value','{applicant.birth_date}')", birth_date)

    waitByMethods.wait_visibility_by_id(driver, 'passport_no')
    passport_no = driver.find_element(By.ID, 'passport_no')
    passport_no.send_keys(applicant.passport_no)

    waitByMethods.wait_visibility_by_id(driver, 'pptIssueDate')
    issue_date = driver.find_element(By.ID, 'pptIssueDate')
    driver.execute_script(f"arguments[0].setAttribute('value','{applicant.issue_date}')", issue_date)

    waitByMethods.wait_visibility_by_id(driver, 'pptExpiryDate')
    exp_date = driver.find_element(By.ID, 'pptExpiryDate')
    driver.execute_script(f"arguments[0].setAttribute('value','{applicant.exp_date}')", exp_date)

    waitByMethods.wait_visibility_by_id(driver, 'pptIssuePalace')
    issue_place = driver.find_element(By.ID, 'pptIssuePalace')
    issue_place.send_keys(applicant.issue_place)


def time_slot_selection(driver: webdriver):
    day = driver.find_element(By.CSS_SELECTOR, "td.day.activeClass[title='Book']")
    day.click()

    waitByMethods.wait_visibility_by_id(driver, 'app_time')
    time_slots = driver.find_element(By.ID, 'app_time')
    select = Select(time_slots)
    random_index = random.randint(1, len(select.options) - 1)
    select.select_by_index(random_index)


def check_site_is_working(driver: webdriver):
    timeout = 60
    starting_time = time.time()

    while time.time() - starting_time < timeout:
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(ec.visibility_of_element_located((By.ID, 'centre')))
            current_time = datetime.now()
            print(f"[INFO] {current_time} ---> Site is working!")
            break
        except (NoSuchElementException, TimeoutException, ElementNotVisibleException, ElementNotInteractableException,
                ElementClickInterceptedException):
            current_time = datetime.now()
            print(f"[ERROR] {current_time} ---> Site was broken!")
            driver.refresh()
            time.sleep(10)


def applicant_booking_normal(applicant: spainApplicants.Applicant):
    current_timestamp = datetime.now()
    print(f"[INFO] {current_timestamp} ---> Processing applicant ---> {applicant.email}")
    # driver_bls = webdriver.Safari()
    driver_bls = webdriver.Chrome(options=option)
    # todo: ИЗМЕНЯТЬ ССЫЛКУ ТУТ
    driver_bls.get(BLS_SPAIN_URL)
    # driver_bls.get(TEST_URL)
    driver_bls.maximize_window()

    driver_yandex = webdriver.Safari()
    # driver_yandex = webdriver.Chrome(options=option)
    driver_yandex.get(YANDEX_URL)
    # driver_yandex.maximize_window()

    check_site_is_working(driver_bls)
    refresh_page_before_bls_captcha_is_working(driver_bls, applicant)
    fill_first_form(driver_bls, 'Normal', applicant)
    input_otp_and_continue(driver_bls, check_email(driver_yandex, applicant), applicant)
    # todo: Комментирую для тестов
    refresh_page_before_element_visible_by_class_name(driver_bls, 'day activeClass', applicant)
    # todo: проверить, что выбор слота вообще работает
    time_slot_selection(driver_bls)
    time.sleep(1)
    fill_second_form(driver_bls, applicant)
    continue_after_second_form(driver_bls, applicant)
    WebDriverWait(driver_bls, WAIT_TIMEOUT).until(ec.alert_is_present).accept()


def applicant_booking_premium(applicant: spainApplicants.Applicant):
    current_timestamp = datetime.now()
    print(f"[INFO] {current_timestamp} ---> Processing applicant ---> {applicant.email}")
    # driver_bls = webdriver.Safari()
    driver_bls = webdriver.Chrome(options=option)
    # todo: ИЗМЕНЯТЬ ССЫЛКУ ТУТ
    driver_bls.get(BLS_SPAIN_URL)
    driver_bls.maximize_window()

    # driver_yandex = webdriver.Safari()
    driver_yandex = webdriver.Chrome(options=option)
    driver_yandex.get(YANDEX_URL)
    # driver_yandex.maximize_window()

    check_site_is_working(driver_bls)
    refresh_page_before_bls_captcha_is_working(driver_bls, applicant)
    fill_first_form(driver_bls, 'Premium', applicant)
    input_otp_and_continue(driver_bls, check_email(driver_yandex, applicant), applicant)
    # todo: Комментирую для тестов
    refresh_page_before_element_visible_by_class_name(driver_bls, 'day activeClass', applicant)
    # todo: проверить, что выбор слота вообще работает
    time_slot_selection(driver_bls)
    fill_second_form(driver_bls, applicant)
    continue_after_second_form(driver_bls, applicant)
    WebDriverWait(driver_bls, 30).until(ec.alert_is_present).accept()


def multiprocessing_applicants_start(applicants_list: list, category_type: str):
    number_of_proc = len(applicants_list)
    pool = multiprocessing.Pool(processes=number_of_proc)

    starting_time = datetime.now()

    if category_type == 'Normal':
        pool.map(applicant_booking_normal, applicants_list)
    else:
        pool.map(applicant_booking_premium, applicants_list)

    ending_time = datetime.now()

    print('Duration: {}'.format(ending_time - starting_time))


def main():
    # applicants_normal_only = [spainApplicants.anzorov]
    # applicants_normal = [spainApplicants.mariia, spainApplicants.nadezhda, spainApplicants.anzorov]
    applicants_premium = [spainApplicants.mariia, spainApplicants.nadezhda, spainApplicants.katerina]
    # applicants_premium = [spainApplicants.mariia]

    while True:
        try:
            multiprocessing_applicants_start(applicants_premium, 'Premium')
            # multiprocessing_applicants_start(applicants_all_types, 'Premium')
        except Exception as e:
            current_time = datetime.now()
            print(f"[ERROR] {current_time} ---> An error occured: {str(e)}")
            print(f"[INFO] {current_time} ---> Restarting the script in 10 seconds...")
            time.sleep(10)

    # multiprocessing_applicants_start(applicants_premium, 'Premium')
    # multiprocessing_applicants_start(applicants_all_types, 'Premium')

    # current_time = datetime.now()
    # print(f"[ERROR] {current_time} ---> An error occured: {str(e)}")
    # print(f"[INFO] {current_time} ---> Restarting the script in 10 seconds...")
    # time.sleep(10)


if __name__ == '__main__':
    main()
