import time
import random
from bs4 import BeautifulSoup
from datetime import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from twocaptcha import TwoCaptcha
import waitByMethods
import frenchApplicants

VFS_GLOBAL_FRA_URL = 'https://visa.vfsglobal.com/rus/ru/fra/login'
WAIT_TIMEOUT = 10
API_KEY = 'a8c29c48cfc7bd56a2519f4584961fa1'
sitekey = '6LfDUY8bAAAAAPU5MWGT_w0x5M-8RdzC29SClOfI'

# option = webdriver.Firefox()
option = webdriver.ChromeOptions()
option.add_experimental_option('detach', True)

centres = {
    'Irkutsk': ' France Visa Application Centre-Irkutsk ',
    'Kaliningrad': ' France Visa Application Centre-Kaliningrad ',
    'Kazan': ' France Visa Application Centre-Kazan ',
    'Khabarovsk': ' France Visa Application Centre-Khabarovsk ',
    'Krasnodar': ' France Visa Application Centre-Krasnodar ',
    'Krasnoyarsk': ' France Visa Application Centre-Krasnoyarsk ',
    'Moscow': ' France Visa Application Centre-Moscow ',
    'Nizhniy Novgorod': ' France Visa Application Centre-Nizhniy Novgorod ',
    'Novosibirsk': ' France Visa Application Centre-Novosibirsk ',
    'Omsk': ' France Visa Application Centre-Omsk ',
    'Perm': ' France Visa Application Centre-Perm ',
    'Rostov on Don': ' France Visa Application Centre-Rostov on Don ',
    'Samara': ' France Visa Application Centre-Samara ',
    'Saratov': ' France Visa Application Centre-Saratov ',
    'St Petersburg': ' France Visa Application Centre-St Petersburg ',
    'Ufa': ' France Visa Application Centre-Ufa ',
    'Vladivistok': ' France Visa Application Centre-Vladivostok ',
    'Yekaterinburg': ' France Visa Application Centre-Yekaterinburg '
}

centres_id = {
    'Irkutsk': 'mat-option-0',
    'Kaliningrad': 'mat-option-1',
    'Kazan': 'mat-option-2',
    'Khabarovsk': 'mat-option-3',
    'Krasnodar': 'mat-option-4',
    'Krasnoyarsk': 'mat-option-5',
    'Moscow': 'mat-option-6',
    'Nizhniy Novgorod': 'mat-option-7',
    'Novosibirsk': 'mat-option-8',
    'Omsk': 'mat-option-9',
    'Perm': 'mat-option-10',
    'Rostov on Don': 'mat-option-11',
    'Samara': 'mat-option-12',
    'Saratov': 'mat-option-13',
    'St Petersburg': 'mat-option-14',
    'Ufa': 'mat-option-15',
    'Vladivistok': 'mat-option-16',
    'Yekaterinburg': 'mat-option-17'
}

categories = {
    'Long': ' Long Stay ',
    'Short': ' Short Stay '
}

categories_id = {
    'Long': 'mat-option-25',
    'Short': 'mat-option-26'
}

subcategories = {
    'All': ' Short Stay All kind of other short stay visas ',
    'Spouse': ' Short Stay children of spouse of French/EU/EEA/CH/UK ',
    'Prime': ' PRIME TIME (55 euros ) Short Stay All kind of other short stay visas '
}

subcategories_id = {
    'All': 'mat-option-28',
    'Spouse': 'mat-option-29',
    'Prime': ' PRIME TIME (55 euros ) Short Stay All kind of other short stay visas '
}


def is_re_captcha(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]')
        return True
    except NoSuchElementException:
        return False


def do_element_visible(driver: webdriver):
    script = """
    var textarea = document.getElementById("g-recaptcha-response");
    if (textarea) {
        textarea.style.width = "100%";
        textarea.style.height = "400px";
        textarea.style.border = "1px solid rgb(193, 193, 193)";
        textarea.style.margin = "100px 25px";
        textarea.style.padding = "0px";
        textarea.style.resize = "none";
        textarea.style.removeProperty('display');  // Set display to "block" to make it visible
    }
    """

    driver.execute_script(
        script
    )


def recaptcha_solver(driver: webdriver,
                     input_sitekey: str,
                     input_url: str,
                     applicant: frenchApplicants.Applicant,
                     prefix_callback_function: str):
    start_time = datetime.now()
    solver = TwoCaptcha(API_KEY)

    current_time = datetime.now()
    print(f'[INFO] {current_time} ---> Solving VFS reCAPTCHA for ---> {applicant.email}')
    key = solver.recaptcha(sitekey=input_sitekey, url=input_url)['code']
    end_time = datetime.now()
    current_time = datetime.now()
    print(
        f'[INFO] {current_time} ---> VFS reCAPTCHA was solved by: {end_time - start_time} for ---> {applicant.email}')

    g_recaptcha_response_name = 'g-recaptcha-response'

    do_element_visible(driver)

    g_recaptcha_input_field = driver.find_element(By.NAME, g_recaptcha_response_name)
    g_recaptcha_input_field.send_keys(key)
    time.sleep(1)

    driver.execute_script(
        f"{prefix_callback_function}.callback('{key}')"
    )


def login(driver: webdriver, applicant: frenchApplicants.Applicant):
    target_email_id = 'mat-input-0'
    target_password_id = 'mat-input-1'
    target_booking_xpath = '//button[contains(span, "Войти")]'

    prefix_callback_function = '___grecaptcha_cfg.clients[0].P.P'

    waitByMethods.wait_visibility_by_id(driver, target_email_id)
    input_email = driver.find_element(By.ID, target_email_id)
    input_email.send_keys(applicant.login_email)

    input_password = driver.find_element(By.ID, target_password_id)
    input_password.send_keys(applicant.password_vfs)

    recaptcha_solver(driver, sitekey, VFS_GLOBAL_FRA_URL, applicant, prefix_callback_function)

    button_booking = driver.find_element(By.XPATH, target_booking_xpath)
    button_booking.click()
    current_time = datetime.now()
    print(f"[INFO] {current_time} ---> Logged in successfully for ---> {applicant.login_email}")


def click_on_the_button_by_xapth(driver: webdriver, xpath: str):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    button = driver.find_element(By.XPATH, xpath)
    driver.execute_script(
        "arguments[0].click();", button
    )


def click_on_the_button_by_class_name(driver: webdriver, class_name: str):
    waitByMethods.wait_vilibility_by_class_name(driver, class_name)
    button = driver.find_element(By.CLASS_NAME, class_name)
    button.click()


def fill_centre_category_subcategory(driver: webdriver, centre_name: str, booking_category: str, subcategory: str):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    target_select_centre_id = 'mat-select-value-1'
    waitByMethods.wait_clickable_by_id(driver, target_select_centre_id)
    driver.find_element(By.ID, target_select_centre_id).click()
    target_centre = f"//span[text() = '{centres[centre_name]}']"
    waitByMethods.wait_clickable_by_xpath(driver, target_centre)
    driver.find_element(By.XPATH, target_centre).click()
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')

    target_select_category_id = 'mat-select-value-3'
    driver.find_element(By.ID, target_select_category_id).click()
    target_category = f"//span[text() = '{categories[booking_category]}']"
    waitByMethods.wait_clickable_by_xpath(driver, target_category)
    driver.find_element(By.XPATH, target_category).click()
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')

    target_select_subcategory_id = 'mat-select-value-5'
    driver.find_element(By.ID, target_select_subcategory_id).click()
    target_subcategory = f"//span[text() = '{subcategories[subcategory]}']"
    waitByMethods.wait_clickable_by_xpath(driver, target_subcategory)
    driver.find_element(By.XPATH, target_subcategory).click()
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')


def fill_subcategory(driver: webdriver, subcategory: str):
    target_select_subcategory_id = 'mat-select-value-5'
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    driver.find_element(By.ID, target_select_subcategory_id).click()

    target_subcategory = f"//span[text() = '{subcategories[subcategory]}']"
    waitByMethods.wait_clickable_by_xpath(driver, target_subcategory)
    element = driver.find_element(By.XPATH, target_subcategory)
    driver.execute_script("arguments[0].click();", element)

    # driver.find_element(By.XPATH, target_subcategory).click()


def find_available_slots(driver: webdriver):
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        ec.visibility_of_all_elements_located(
            (By.XPATH, "//div[contains(.,' Самый ранний доступный слот записи')]"))
    )


def refresh_page_until_slot_will_be_available_for_selected_city(driver: webdriver, city: str, is_prime_available: bool):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    timeout = 60
    start_time = time.time()
    selected_short = 'Short'
    selected_all = 'All'
    selected_prime = 'Prime'
    selected_spouse = 'Spouse'

    waitByMethods.wait_visibility_by_id(driver, 'mat-select-0')
    while time.time() - start_time < timeout:
        if is_prime_available:
            try:
                current_time = datetime.now()
                print(
                    f"[INFO] {current_time} ---> Selected city: {city} --> Subcategory: {subcategories[selected_all]}")
                fill_centre_category_subcategory(driver, city, selected_short, selected_all)
                waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
                find_available_slots(driver)
                current_time = datetime.now()
                print(f"[INFO] {current_time} ---> Available slots founded in {city} for {subcategories[selected_all]}")
                break
            except (TimeoutException, NoSuchElementException):
                current_time = datetime.now()
                print(f"[INFO] {current_time} ---> No available slots in {city} for {subcategories[selected_all]}")
                print(
                    f"[INFO] {current_time} ---> Selected city: {city} --> Subcategory: {subcategories[selected_prime]}")
                try:
                    fill_subcategory(driver, selected_prime)
                    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
                    find_available_slots(driver)
                    current_time = datetime.now()
                    print(
                        f"[INFO] {current_time} ---> Available slots founded in {city} for {subcategories[selected_prime]}")
                    break
                except TimeoutException:
                    current_time = datetime.now()
                    print(
                        f"[INFO] {current_time} ---> No available slots in {city} for {subcategories[selected_prime]}")
                    print(
                        f"[INFO] {current_time} ---> Selected city: {city} --> Subcategory: {subcategories[selected_spouse]}")
                    try:
                        fill_subcategory(driver, selected_spouse)
                        waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
                        find_available_slots(driver)
                        current_time = datetime.now()
                        print(
                            f"[INFO] {current_time} ---> Available slots founded in {city} for {subcategories[selected_spouse]}")
                        break
                    except TimeoutException:
                        print(
                            f"[INFO] {current_time} No available slots in {city} for {subcategories[selected_spouse]}")
                        continue
        else:
            try:
                current_time = datetime.now()
                print(
                    f"[INFO] {current_time} ---> Selected city: {city} --> Subcategory: {subcategories[selected_all]}")
                fill_centre_category_subcategory(driver, city, selected_short, selected_all)
                waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
                find_available_slots(driver)
                current_time = datetime.now()
                print(f"[INFO] {current_time} ---> Available slots founded in {city} for {subcategories[selected_all]}")
                break
            except TimeoutException:
                current_time = datetime.now()
                print(f"[INFO] {current_time} ---> No available slots in {city} for {subcategories[selected_all]}")
                print(
                    f"[INFO] {current_time} ---> Selected city: {city} --> Subcategory: {subcategories[selected_spouse]}")
                try:
                    fill_subcategory(driver, selected_spouse)
                    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
                    find_available_slots(driver)
                    current_time = datetime.now()
                    print(
                        f"[INFO] {current_time} ---> Available slots founded in {city} for {subcategories[selected_spouse]}")
                    break
                except TimeoutException:
                    print(f"[INFO] {current_time} No available slots in {city} for {subcategories[selected_spouse]}")
                    continue


def fill_about_me_info(driver: webdriver, applicant: frenchApplicants.Applicant):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    name_id = 'mat-input-2'
    surname_id = 'mat-input-3'
    gender_id = 'mat-select-value-7'
    target_gender_xpath = f"//span[contains(.,'{applicant.gender}')]"
    date_of_birth_id = 'dateOfBirth'
    citizen_id = 'mat-select-value-9'
    target_citizen_xpath = f"//span[text() = ' RUSSIAN FEDERATION ']"
    passport_no_id = 'mat-input-4'
    passport_expiration_date = 'passportExpirtyDate'
    code_id = 'mat-input-5'
    phone_no = 'mat-input-6'
    email_id = 'mat-input-7'

    time.sleep(2)
    driver.find_element(By.ID, gender_id).click()
    waitByMethods.wait_clickable_by_xpath(driver, target_gender_xpath)
    driver.find_element(By.XPATH, target_gender_xpath).click()
    time.sleep(2)

    driver.find_element(By.ID, citizen_id).click()
    waitByMethods.wait_clickable_by_xpath(driver, target_citizen_xpath)
    element = driver.find_element(By.XPATH, target_citizen_xpath)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)

    waitByMethods.wait_clickable_by_id(driver, name_id)
    driver.find_element(By.ID, name_id).send_keys(applicant.first_name)
    time.sleep(3)
    driver.find_element(By.ID, surname_id).send_keys(applicant.last_name)
    time.sleep(3)
    driver.find_element(By.ID, date_of_birth_id).send_keys(applicant.birth_date)
    time.sleep(3)
    driver.find_element(By.ID, passport_no_id).send_keys(applicant.passport_no)
    time.sleep(3)
    driver.find_element(By.ID, passport_expiration_date).send_keys(applicant.exp_date)
    time.sleep(2)
    driver.find_element(By.ID, code_id).send_keys(applicant.code)
    time.sleep(2)
    driver.find_element(By.ID, phone_no).send_keys(applicant.phone)
    time.sleep(2)
    driver.find_element(By.ID, email_id).send_keys(applicant.email)
    time.sleep(5)

    target_save_xpath = '//button[contains(span, "Сохранить")]'
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')

    click_on_the_button_by_xapth(driver, target_save_xpath)

    print("ok")


def info_about_me_confirm(driver: webdriver):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    target_continue_xpath = '//button[contains(span, "Продолжить")]'
    click_on_the_button_by_xapth(driver, target_continue_xpath)


# todo: here I stopped
def select_date(driver: webdriver):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')

    pre_script = """
    tables = document.getElementsByClassName('fc-scrollgrid-sync-table');
    tbodies = tables[0].getElementsByTagName('tbody');
    tds = tables[0].getElementsByTagName('td');
    return tds;
    """

    tds = driver.execute_script(
        pre_script
    )
    print(tds)
    time.sleep(1)

    data_dates = []

    for td in tds:
        td_html = td.get_attribute('outerHTML')
        soup = BeautifulSoup(td_html, 'html.parser')
        date_element = soup.find(class_='date-availiable')
        if date_element:
            data_date = date_element.get('data-date')
            data_dates.append(data_date)
        else:
            # data_dates.append("Date not found!")
            continue

    print(data_dates)

    filtered_date_dates = [item for item in data_dates if item.startswith("2023")]
    # filtered_date_dates = [item for item in data_dates if item.startswith("2023") and item != ""]

    main_script = '''
    calendar = document.getElementsByTagName("full-calendar")[0].__ngContext__[158].calendar;
    calendar.select("REPLACEME")
    calendar.trigger("dateClick", {dateStr: "REPLACEME"})
    '''

    modified_main_script = main_script.replace('"REPLACEME"', f'"{filtered_date_dates[0]}"')

    driver.execute_script(
        modified_main_script
    )

    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    # radio_elements = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][name='SlotRadio'].ba-slot-radio.active")

    radio_elements = driver.find_elements(By.NAME, "SlotRadio")
    random_index = random.randint(0, len(radio_elements) - 1)
    random_radio_id = radio_elements[random_index].get_attribute("id")
    driver.execute_script(
        f"document.getElementById('{random_radio_id}').click()"
    )
    time.sleep(2)

    # Randomly select one element from the list
    # random_radio_element = random.choice(radio_elements)
    # if random_radio_element:
    #     random_radio_element.click()
    # else:
    #     current_time = datetime.now()
    #     print(f"[ERROR] {current_time} ---> No available time slots!")

    # if radio_elements:
    #     random_index = random.randint(0, len(radio_elements) - 1)
    #     radio_elements[random_index].click()

    target_continue_xpath = '//button[contains(span, "Продолжить")]'
    click_on_the_button_by_xapth(driver, target_continue_xpath)
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')


def select_services(driver: webdriver):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    target_continue_xpath = '//button[contains(span, "Продолжить")]'
    waitByMethods.wait_clickable_by_xpath(driver, target_continue_xpath)
    click_on_the_button_by_xapth(driver, target_continue_xpath)
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    print("ok")


def skip_insurance_details(driver: webdriver):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    driver.find_element(By.ID, 'onetrust-close-btn-container').click()
    target_continue_xpath = '//button[contains(span, "Продолжить")]'
    waitByMethods.wait_clickable_by_xpath(driver, target_continue_xpath)
    click_on_the_button_by_xapth(driver, target_continue_xpath)
    target_confirm_xpath = '//button[contains(span, "Подтвердить")]'
    waitByMethods.wait_visibility_by_xpath(driver, target_confirm_xpath)
    driver.find_element(By.XPATH, target_confirm_xpath).click()
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')


def details_and_payment(driver: webdriver):
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')
    driver.execute_script("document.getElementById('mat-checkbox-3-input').click()")
    target_payment_online_xpath = '//button[contains(span, "Оплатить онлайн")]'
    driver.find_element(By.XPATH, target_payment_online_xpath).click()
    target_continue_xpath = '//button[contains(span, "Продолжить")]'
    waitByMethods.wait_clickable_by_xpath(driver, target_continue_xpath)
    driver.find_element(By.XPATH, target_continue_xpath).click()
    waitByMethods.wait_invisibility_by_class_name(driver, 'sk-ball-spin-clockwise')


def booking(applicant: frenchApplicants.Applicant, city: str, is_prime_exist: bool):
    current_time = datetime.now()
    print(f"[INFO] {current_time} ---> Processing applicant: {applicant.email}")

    driver_vfs = webdriver.Chrome(options=option)
    # driver_vfs = webdriver.Firefox()
    driver_vfs.get(VFS_GLOBAL_FRA_URL)
    driver_vfs.maximize_window()
    time.sleep(10)

    login(driver_vfs, applicant)

    target_create_booking_xpath = '//button[contains(span, "Записаться на прием")]'
    target_continue_xpath = '//button[contains(span, "Продолжить")]'

    click_on_the_button_by_xapth(driver_vfs, target_create_booking_xpath)
    refresh_page_until_slot_will_be_available_for_selected_city(driver_vfs, city, is_prime_exist)
    click_on_the_button_by_xapth(driver_vfs, target_continue_xpath)
    fill_about_me_info(driver_vfs, applicant)
    info_about_me_confirm(driver_vfs)

    # todo: тут остановился, ниже не работает ничего
    select_date(driver_vfs)

    select_services(driver_vfs)

    skip_insurance_details(driver_vfs)

    details_and_payment(driver_vfs)


if __name__ == '__main__':
    moscow = 'Moscow'
    yekat = 'Yekaterinburg'
    # is_prime = True
    is_prime = False
    try:
        booking(frenchApplicants.test_user_2, yekat, is_prime)
    except NoSuchElementException:
        current_timestamp = datetime.now()
        print(f"[ERROR] {current_timestamp} ---> No such element exception!")
