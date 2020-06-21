import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    wd = webdriver.Chrome()
    wd.quit
    return wd


test_data_for_checking_names_and_costs = [
    ('.name', '#box-product .title'),
    ('.regular-price', '#box-product .regular-price'),
    ('.campaign-price', '#box-product .campaign-price')
]


@pytest.mark.parametrize("target_on_main_page,target_on_product_page",
                         test_data_for_checking_names_and_costs)
def test_names_and_costs_products(driver, target_on_main_page, target_on_product_page):
    """
    Тест проверяет совпадение названия и значения цен на главной и странице продукта
    :param driver:
    :param target_on_main_page: локатор для нахождения названия/цены(обычной / акционной)на главной странице
    :param target_on_product_page: локатор для нахождения названия/цены(обычной / акционной)на странице продукта
    :return:
    """

    driver.get("http://www.litecart.com/")
    main_page_element = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li')
    value_on_main_page = ''
    value_on_product_page = ''

    # print('Name of ', i, '-th prod', elements[i].find_element(By.CSS_SELECTOR, '.name').text)
    value_on_main_page += main_page_element.find_element(By.CSS_SELECTOR, target_on_main_page).text
    main_page_element.click()
    value_on_product_page += driver.find_element(By.CSS_SELECTOR, target_on_product_page).text
    # print('Name in prod page of ', i, '-th prod', driver.find_element(By.CSS_SELECTOR, '#box-product .title').text)
    print('List of product titles on main pages', value_on_main_page)
    print('List of product titles on product pages', value_on_product_page)

    assert value_on_main_page == value_on_product_page


def test_color_regular_cost_products_on_main_page(driver):
    """
    Тест проверяет цвет обычной цены на главной странице

    :param driver:
    :return:
    """

    driver.get("http://www.litecart.com/")

    element = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li .regular-price')
    color_string = element.value_of_css_property('color')
    nums = re.findall(r'\d+', color_string)
    colors = [int(i) for i in nums]

    print('color', colors)
    assert colors[0] == colors[1] == colors[2]


def test_color_campaign_cost_products_on_main_page(driver):
    """
    Тест проверяет цвет акционной цены на главной странице
    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")

    element = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li .campaign-price')
    color_string = element.value_of_css_property('color')
    nums = re.findall(r'\d+', color_string)
    colors = [int(i) for i in nums]

    print('color', colors)
    assert colors[1] == colors[2] == 0


def test_color_regular_cost_products_on_product_page(driver):
    """
    Тест проверяет цвет обычной цены на странице продукта

    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")
    driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li').click()

    element = driver.find_element(By.CSS_SELECTOR, '#box-product .regular-price')
    color_string = element.value_of_css_property('color')
    nums = re.findall(r'\d+', color_string)
    colors = [int(i) for i in nums]

    print('color', colors)
    assert colors[0] == colors[1] == colors[2]


def test_color_campaign_cost_products_on_product_page(driver):
    """
    Тест проверяет цвет акционной цены на странице продукта
    """

    driver.get("http://www.litecart.com/")
    driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li').click()

    element = driver.find_element(By.CSS_SELECTOR, '#box-product .campaign-price')
    color_string = element.value_of_css_property('color')
    nums = re.findall(r'\d+', color_string)
    colors = [int(i) for i in nums]

    print('color', colors)
    assert colors[1] == colors[2] == 0


def test_text_style_regular_cost_products_on_main_page(driver):
    """
    Тест проверяет что для обычной цены на главной странице используется зачеркнтый шрифт
    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")

    element = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li .regular-price')
    text_decoration = element.value_of_css_property('text-decoration-line')

    print('text_decoration ', text_decoration)
    assert text_decoration == 'line-through'


def test_text_style_campaign_cost_products_on_main_page(driver):
    """
    Тест проверяет что для акционной цены на главной странице используется жирный шрифт
    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")

    element = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li .campaign-price')
    font_weight = element.value_of_css_property('font-weight')

    print('font_weight', font_weight)
    assert font_weight == '700'


def test_text_style_regular_cost_products_on_product_page(driver):
    """
    Тест проверяет что для обычной цены на странице продукта используется зачеркнутый шрифт
    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")

    driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li').click()
    element = driver.find_element(By.CSS_SELECTOR, '#box-product .regular-price')
    text_decoration = element.value_of_css_property('text-decoration-line')

    print('text_decoration ', text_decoration)
    assert text_decoration == 'line-through'


def test_text_style_campaign_cost_products_on_product_page(driver):
    """
    Тест проверяет что для акционной цены на странице продукта используется жирный шрифт
    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")

    driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li').click()
    element = driver.find_element(By.CSS_SELECTOR, '#box-product .campaign-price')
    font_weight = element.value_of_css_property('font-weight')

    print('font_weight', font_weight)
    assert font_weight == '700'


def test_comparing_cost_text_size_on_main_page(driver):
    """
    Тест проверяет что для размер шрифта обычной цены меньше размера шрифта акционной цены
    на главной продукта
    :param driver:
    :return:
    """
    driver.get("http://www.litecart.com/")

    regular_cost = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li .regular-price')
    text_size_regular_cost = regular_cost .value_of_css_property('font-size')
    campaign_cost = driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li .campaign-price')
    text_size_campaign_cost = campaign_cost .value_of_css_property('font-size')

    print('text_size_regular_cost:', text_size_regular_cost, 'text_size_campaign_cost ', text_size_campaign_cost )
    assert text_size_regular_cost < text_size_campaign_cost


def test_comparing_cost_text_size_on_product_page(driver):
    """
        Тест проверяет что для размер шрифта обычной цены меньше размера шрифта акционной цены
        на странице продукта
        :param driver:
        :return:
        """
    driver.get("http://www.litecart.com/")

    driver.find_element(By.CSS_SELECTOR, '#box-campaigns ul > li').click()
    regular_cost = driver.find_element(By.CSS_SELECTOR, '#box-product .regular-price')
    text_size_regular_cost = regular_cost.value_of_css_property('font-size')
    campaign_cost = driver.find_element(By.CSS_SELECTOR, '#box-product .campaign-price')
    text_size_campaign_cost = campaign_cost.value_of_css_property('font-size')

    print('text_size_regular_cost:', text_size_regular_cost, 'text_size_campaign_cost ', text_size_campaign_cost)
    assert text_size_regular_cost < text_size_campaign_cost
