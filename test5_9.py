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


def test_countries(driver):
    link = "http://www.litecart.com/admin/?app=countries&amp;doc=countries"
    test_driver = login(driver, link)
    countries_links = test_driver.find_elements(By.CSS_SELECTOR, '.dataTable .row a:not([title="Edit"])')
    countries = []
    contries_for_checking = []
    for link in countries_links:
        countries.append(link.text)
    contries_for_checking = countries.copy()
    contries_for_checking.sort()
    for i, country in enumerate(countries):
        if contries_for_checking[i] == country:
            print('For', i, '-th value', country, 'pass')
        else:
            print('For', i, '-th value', country, 'FAIL')
        assert contries_for_checking[i] == country


test_data_for_checking_sorting = [
    ('countries&amp;doc=countries',
     'Name',
     ') :not([value=""])',
     'countries'
     ),
    ('geo_zones&doc=geo_zones',
     'Zone',
     ') option[selected]',
     'geo_zone'
     )
]


@pytest.mark.parametrize("target,header_text,end_locator_for_zones,start_page",
                         test_data_for_checking_sorting)
def test_dda_geozones(driver,
                  target,
                  header_text,
                  end_locator_for_zones,
                  start_page):
    '''

    :param driver:
    :param target:  окончание ссылки для функции get
    :param header_text: текст для пределения колонки для поиска названия зон/стран
    :param end_locator_for_zones: отличие в локаторе для поиска зон/стран
    :param start_page:  часть ссылки для возрата к начальной странице теста
    :return:
    '''
    link = 'http://www.litecart.com/admin/?app=' + target
    test_driver = login(driver, link)
    headers = test_driver.find_elements(By.CSS_SELECTOR, '.dataTable .header th')
    number_column_of_zones = 0
    for i, header in enumerate(headers):
        if header.text == "Zones":
            # print(header.text)
            number_column_of_zones = i + 1
            break
    geozones = test_driver.find_elements(
        By.CSS_SELECTOR, '.dataTable .row :nth-child(' + str(number_column_of_zones) + ')')
    numbers_links = []
    for i, geozone in enumerate(geozones):
        if geozone.text != '0':
            numbers_links.append(i)
    for number in numbers_links:
        countries_links = test_driver.find_elements(By.CSS_SELECTOR, '.dataTable .row a:not([title="Edit"])')
        name_counrty = countries_links[number].text
        countries_links[number].click()
        number_column_of_names = 0
        headers_zones = test_driver.find_elements(By.CSS_SELECTOR, '.dataTable .header th')
        for i, header in enumerate(headers_zones):
            if header.text == header_text:
                number_column_of_names = i + 1
                break
        locator_for_zones = '.dataTable tr:not(.header) td:nth-child(' + \
                            str(number_column_of_names) + \
                            end_locator_for_zones
        namezones = test_driver.find_elements(By.CSS_SELECTOR, locator_for_zones)
        namezones_list = []
        namezones_list_for_checking = []
        for i, namezone in enumerate(namezones):
            namezones_list.append(namezone.text)
        namezones_list_for_checking = namezones_list.copy()
        namezones_list_for_checking.sort()
        # print('Zones:', namezones_list, '\nZones_sorted', namezones_list_for_checking)
        for i, namezone_item, in enumerate(namezones_list):
            if namezones_list_for_checking[i] == namezone_item:
                print('For', i, '-th value', namezone_item, 'for country', name_counrty, 'pass', )
            else:
                print('For', i, '-th value', namezone_item, 'for country', name_counrty, 'FAIL', )
            assert namezones_list_for_checking[i] == namezone_item
        locator_back_to_startpage = 'ul > li#app- > a[href*=' + start_page + ']'
        test_driver.find_element(By.CSS_SELECTOR, locator_back_to_startpage).click()
