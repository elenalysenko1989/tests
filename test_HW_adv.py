# from base64 import encode
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
# from get_excel_data import login_form_parameters
from get_db_data  import login_form_parameters
import logging

logging.basicConfig(filename=r'C:\Users\elena\OneDrive\Documents\WebDriver\Selenium\Project\tests\logs\info.log',
                    encoding='utf-8',
                    level=logging.INFO,
                    force=True,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%y %I:%M:%S %p')


#### COMMON FUNCTIONS ####
def test_login_vc():
    logging.info('Login with valid credentials')
    global driver
    driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    # driver = webdriver.Firefox(executable_path=r'C:\WebDriver\geckodriver.exe')
    driver.get('https://www.saucedemo.com/')
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.ID, 'login-button').click()

def test_add_i_to_cart():
        test_login_vc()
        product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
        product_names[0].click()
        driver.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()

def capture_evidence():
    image_name = fr"C:\Users\elena\OneDrive\Documents\WebDriver\Selenium\Project\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png" 
    driver.save_screenshot(image_name)

def text_is_displayed(text):
    logging.info(f'Checking if {text} exists on the page')
    return text.lower() in driver.page_source.lower()

#### TEST CASES ####

# login_form_parameters = [
#     ('locked_out_user', 'secret_sauce',  'Sorry, this user has been locked out'),
#     ('test', 'test',  'Username and password do not match any user in this service')
#     ]
@pytest.mark.parametrize("username, password, checkpoint", login_form_parameters)  
def test_login_invalid_credentials(username, password, checkpoint):
    global driver
    driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    driver.get('https://www.saucedemo.com/')
    if username != None: driver.find_element(By.ID, 'user-name').send_keys(username)
    if password != None:driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'login-button').click()
    sleep(5)
    assert text_is_displayed(checkpoint)
    capture_evidence()
    driver.quit()

####################################################
@pytest.fixture()
def setup(request):
    test_login_vc()


    def teardown():
        capture_evidence()
        driver.quit()
    request.addfinalizer(teardown)

#####################################################

def test_login_valid_credentials(setup):
    assert text_is_displayed('products')
   

def test_view_product_details(setup):
     product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
     product_names[0].click()
     assert text_is_displayed('back to products')
   

def test_add_item_to_cart(setup):
     product_names = driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
     product_names[0].click()
     driver.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()
     assert text_is_displayed('remove')

def test_click_cart_icon(setup):
    test_add_i_to_cart()
    driver.find_element(By.CSS_SELECTOR, '.shopping_cart_link').click()
    assert text_is_displayed('your cart')

    
