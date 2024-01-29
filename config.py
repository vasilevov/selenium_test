from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
email = 'testmail@yandex.ru'
password = '12345678'

def login():
    driver.get('https://qa-mesto.praktikum-services.ru/')
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, ".//button[@class='auth-form__button']").click()
    WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'profile__description')))

def wait(time):
    WebDriverWait(driver, time).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'profile__description')))

def get_cardname_with_time():
    current_time = time.strftime("%H:%M:%S-%d.%m.%Y", time.localtime())
    return "Москва " + current_time

def get_last_card():
    list_of_cards = driver.find_elements(By.XPATH, ".//li[@class='places__item card']")
    return list_of_cards[list_of_cards.__len__() - 1]