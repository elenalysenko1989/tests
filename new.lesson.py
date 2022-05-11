import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep

driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
driver.get('https://www.saucedemo.com/')
driver.find_element(By.ID, 'user-name').send_keys('standard_user')
driver.find_element(By.ID, 'password').send_keys('secret_sauce')
driver.find_element(By.ID, 'login-button').click()
# driver.find_element(By.CLASS_NAME, 'submit-button').click()

def test_add_item_to_cart():
     product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
     product_names[0].click()
     driver.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()
test_add_item_to_cart()
element = driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
print(element.text == '1')
driver.find_element(By.CSS_SELECTOR, '.shopping_cart_link').click()
price = driver.find_element(By.CSS_SELECTOR, '.inventory_item_price')
print(price.text)

