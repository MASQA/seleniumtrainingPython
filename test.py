import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    wd = webdriver.Chrome()
    wd.quit
    return wd


test_data_links_first_level = [
    ('1', 'Template'),
    ('2', 'Catalog'),
    ('3', 'Countries'),
    ('4', 'Currencies'),
    ('5', 'Customers'),
    ('6', 'Geo Zones'),
    ('7', 'Languages'),
    ('8', 'Job Modules'),
    ('9', 'Orders'),
    ('10', 'Pages'),
    ('11', 'Monthly Sales'),
    ('12', 'Settings'),
    ('13', 'Slides'),
    ('14', 'Tax Classes'),
    ('15', 'Search Translations'),
    ('16', 'Users'),
    ('17', 'vQmods'),
]


def login(driver):
    driver.get("http://www.litecart.com/admin/")
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.logotype')))
    return driver


@pytest.mark.parametrize("number_link,header_value", test_data_links_first_level)
def test_sidebar_links_first_levev(driver, number_link, header_value):
    test_driver = login(driver)
    test_driver.find_element(By.CSS_SELECTOR, 'ul:not(.docs) > li:nth-child('+number_link+')').click()
    WebDriverWait(test_driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(),"' + header_value + '")]')))
    test_driver.close()


test_data_links_second_level = [
    ('1', '1', 'Template', 'Template'),
    ('1', '2', 'Template', 'Logotype'),
    ('2', '1', 'Catalog', 'Catalog'),
    ('2', '2', 'Catalog', 'Product Groups'),
    ('2', '3', 'Catalog', 'Option Groups'),
    ('2', '4', 'Catalog', 'Manufacturers'),
    ('2', '5', 'Catalog', 'Suppliers'),
    ('2', '6', 'Catalog', 'Delivery Statuses'),
    ('2', '7', 'Catalog', 'Sold Out Statuses'),
    ('2', '8', 'Catalog', 'Quantity Units'),
    ('2', '9', 'Catalog', 'CSV Import/Export'),
    ('5', '1', 'Customers', 'Customers'),
    ('5', '2', 'Customers', 'CSV Import/Export'),
    ('5', '3', 'Customers', 'Newsletter'),
    ('7', '1', 'Languages', 'Languages'),
    ('7', '2', 'Languages', 'Storage Encoding'),
    ('8', '1', 'Job Modules', 'Job Modules'),
    ('8', '2', 'Job Modules', 'Customer Modules'),
    ('8', '3', 'Job Modules', 'Shipping Modules'),
    ('8', '4', 'Job Modules', 'Payment Modules'),
    ('8', '5', 'Job Modules', 'Order Total Modules'),
    ('8', '6', 'Job Modules', 'Order Success Modules'),
    ('8', '7', 'Job Modules', 'Order Action Modules'),
    ('9', '1', 'Orders', 'Orders'),
    ('9', '2', 'Orders', 'Order Statuses'),
    ('11', '1', 'Monthly Sales', 'Monthly Sales'),
    ('11', '2', 'Monthly Sales', 'Most Sold Products'),
    ('11', '3', 'Monthly Sales', 'Most Shopping Customers'),
    ('12', '1', 'Settings', 'Settings'),
    ('12', '2', 'Settings', 'Settings'),
    ('12', '3', 'Settings', 'Settings'),
    ('12', '4', 'Settings', 'Settings'),
    ('12', '5', 'Settings', 'Settings'),
    ('12', '6', 'Settings', 'Settings'),
    ('12', '7', 'Settings', 'Settings'),
    ('12', '8', 'Settings', 'Settings'),
    ('14', '1', 'Tax Classes', 'Tax Classes'),
    ('14', '2', 'Tax Classes', 'Tax Rates'),
    ('15', '1', 'Search Translations', 'Search Translations'),
    ('15', '2', 'Search Translations', 'Scan Files For Translations'),
    ('15', '3', 'Search Translations', 'CSV Import/Export'),
    ('17', '1', 'vQmods', 'vQmods')
]


@pytest.mark.parametrize("number_link,number_sub_link,header_for_waiting,header_for_checking",
                         test_data_links_second_level)
def test_sidebar_links_second_level(driver, number_link, number_sub_link,
                                    header_for_waiting, header_for_checking):
    test_driver = login(driver)
    test_driver.find_element(By.CSS_SELECTOR, 'ul:not(.docs) > li:nth-child('+number_link+')').click()
    WebDriverWait(test_driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(),"'+ header_for_waiting+'")]')))
    test_driver.find_element(By.CSS_SELECTOR, 'ul.docs>li:nth-child(' + number_sub_link + ')').click()
    WebDriverWait(test_driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h1[contains(text(),"' + header_for_checking + '")]')))
    test_driver.close()


def test_if_we_must_just_walkthrough_on_sidebar(driver):
    test_driver = login(driver)
    high_level_links = test_driver.find_elements(By.CSS_SELECTOR, 'ul > li#app-')
    quantity_high_level_links = len(high_level_links)
    i_high_level_links = 0
    while i_high_level_links < quantity_high_level_links:
        high_level_links[i_high_level_links].click()
        low_level_links = test_driver.find_elements(By.CSS_SELECTOR, 'ul.docs > li')
        quantity_low_level_links = len(low_level_links)
        i_low_level_links = 0
        WebDriverWait(test_driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//h1')))
        while i_low_level_links < quantity_low_level_links:
            low_level_links[i_low_level_links].click()
            WebDriverWait(test_driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//h1')))
            i_low_level_links += 1
            low_level_links = test_driver.find_elements(By.CSS_SELECTOR, 'ul.docs > li')
        i_high_level_links +=1
        high_level_links = test_driver.find_elements(By.CSS_SELECTOR, 'ul > li#app-')