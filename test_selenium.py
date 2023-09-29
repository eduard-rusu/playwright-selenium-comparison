import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.close()


def test_has_title(driver):
    driver.get("http://playwright.dev")
    assert driver.title == 'Fast and reliable end-to-end testing for modern web apps | Playwright'


def test_navigate_page(driver):
    driver.get("http://playwright.dev")
    el = driver.find_element(By.XPATH, '//*[@id="docusaurus_skipToContent_fallback"]/header/div/div/a')
    nav_el = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul'))
    )

    el.click()
    WebDriverWait(driver, 5).until(
        EC.url_to_be('https://playwright.dev/docs/intro')
    )

    WebDriverWait(driver, 30).until(
        EC.staleness_of(nav_el)
    )
    el = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul')
    assert el.value_of_css_property('visibility') == 'hidden'

    action = ActionChains(driver)

    el = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div'))
    )
    action.move_to_element(el).perform()

    el = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul'))
    )
    assert el.value_of_css_property('visibility') == 'visible'

    el = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul/li[2]'))
    )
    el.click()

    WebDriverWait(driver, 5).until(
        lambda d: d.current_url == 'https://playwright.dev/python/docs/intro'
    )

    el = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/a')
    assert el.get_attribute('innerText') == 'Python'

    el = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[2]/div[2]/button')
    el.click()

    el = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="docsearch-input"]'))
    )
    el.send_keys('Getting Started')

    WebDriverWait(driver, 30).until(
        EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="docsearch-list"]'))
    )
    el.send_keys(Keys.ENTER)

    WebDriverWait(driver, 5).until(
        lambda d: d.current_url == 'https://playwright.dev/python/docs/library'
    )