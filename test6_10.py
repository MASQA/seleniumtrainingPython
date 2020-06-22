import pytest
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
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


def test_sing_up(driver):
    driver.get("http://www.litecart.com/")
    driver.find_element(By.CSS_SELECTOR, 'form[name*=login] a').click()
    now = datetime.datetime.now()
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=firstname]') \
        .send_keys('name_' + str(now.microsecond))
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=lastname]')\
        .send_keys('surname_' + str(now.microsecond))
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=address1]').\
        send_keys('address1_' + str(now.microsecond))
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=postcode]') \
        .send_keys(random.randrange(10000, 99999))
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=city]')\
        .send_keys('city_' + str(now.microsecond))
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] .select2').click()
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=country_code] option[value = US]').click()
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] .select2').click()
    mail = 'mail_' + str(now.microsecond) + '@domain.any'
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=email]').send_keys(mail)
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=phone]') \
        .send_keys('+' + str(random.randrange(10000000000, 99999999999)))
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=password]').send_keys('password')
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=confirmed_password]').send_keys('password')
    driver.find_element(By.CSS_SELECTOR, 'form[name*=customer] [name=create_account]').click()
    driver.find_element(By.CSS_SELECTOR, '#box-account a[href*=logout]').click()
    driver.find_element(By.CSS_SELECTOR, 'form[name*=login] [name=email]').send_keys(mail)
    driver.find_element(By.CSS_SELECTOR, 'form[name*=login] [name=password]').send_keys('password')
    driver.find_element(By.CSS_SELECTOR, 'form[name*=login] [name=login]').click()
    driver.find_element(By.CSS_SELECTOR, '#box-account a[href*=logout]').click()
