import pytest
import datetime
import os
import pathlib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    wd = webdriver.Chrome()
    wd.quit
    return wd


def login(driver, url):
    if url is None:
        driver.get("http://www.litecart.com/admin/")

    else:
        driver.get(url)
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.logotype')))
    return driver


def test_adding_product_in_catalog(driver):
    link = 'http://www.litecart.com/admin/?app=catalog&doc=catalog'
    test_driver = login(driver, link)
    test_driver.find_element(By.CSS_SELECTOR, '#content .button[href*=edit_prod]').click()
    #заполнение табы general
    test_driver.find_element(By.CSS_SELECTOR, 'div.tabs a[href*=general]').click()
    WebDriverWait(test_driver, 50).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name=status]')))
    test_driver.find_element(By.CSS_SELECTOR, 'input[name=status][value="1"]').click()
    now = datetime.datetime.now()
    product_name = 'Product' + str(now.microsecond)
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=name]').send_keys(product_name)
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=code]').send_keys(str(now.microsecond))
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=categories][data-name*=Subcat]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'select[name=default_category_id]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'select[name=default_category_id] > option[value="2"]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=product_groups][value="1-3"]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=quantity]').send_keys(Keys.CONTROL + "a")
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=quantity]').send_keys('2.55')
    filename = Path('picture.png').resolve()
    #print(filename)
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=new_images]').send_keys(str(filename))
    # конец заполнения картинку
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=date_valid_from]').send_keys('01152016')
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=date_valid_to]').send_keys('01252016')
    #заполнение табы информация
    test_driver.find_element(By.CSS_SELECTOR, 'div.tabs a[href*=information]').click()
    WebDriverWait(test_driver, 50).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name*=manufacturer]')))
    test_driver.find_element(By.CSS_SELECTOR, 'select[name*=manufact]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'select[name*=manufact] option[value="1"]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=keywords]')\
        .send_keys('Keywords' + str(now.microsecond))
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=short_description]')\
        .send_keys('Short Description' + str(now.microsecond))
    test_driver.find_element(By.CSS_SELECTOR, '.trumbowyg-editor')\
        .send_keys('Description' + str(now.microsecond))
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=head_title]') \
        .send_keys('Head_title' + str(now.microsecond))
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=meta_description]') \
        .send_keys('Meta_description' + str(now.microsecond))
    #заполнение табы цены
    test_driver.find_element(By.CSS_SELECTOR, 'div.tabs a[href*=prices]').click()
    WebDriverWait(test_driver, 50).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name*=purchase_price]')))
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=purchase_price]').send_keys(Keys.CONTROL + "a")
    test_driver.find_element(By.CSS_SELECTOR, 'input[name*=purchase_price]').send_keys('2.55')
    test_driver.find_element(By.CSS_SELECTOR, 'select[name*=purchase_price]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'select[name*=purchase_price] option[value="USD"]').click()
    test_driver.find_element(By.CSS_SELECTOR, 'button[name*=save]').click()
    #проверка
    test_driver.find_element(By.CSS_SELECTOR, '#app- a[href*="doc=catalog"]').click()
    test_driver.find_element(By.CSS_SELECTOR, '.dataTable a[href*="category_id=1"]:not([title=Edit] )').click()
    test_driver.find_element(By.CSS_SELECTOR, '.dataTable a[href*="category_id=2"]:not([title=Edit] )').click()
    test_driver.find_element(By.XPATH, '//a[contains(text(),"' + product_name +'")]')



