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


def test_list_of_offer_on_page(driver):
    driver.get("http://www.litecart.com/")
    root_elements = driver.find_elements(By.CSS_SELECTOR, '.product')
    for element in root_elements:
        nested_elements = element.find_elements(By.CSS_SELECTOR, '.sticker')
        assert len(nested_elements) == 1





