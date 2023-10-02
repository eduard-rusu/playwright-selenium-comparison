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


#def test_has_title(driver):
#    driver.get("http://playwright.dev")
#    assert driver.title == 'Fast and reliable end-to-end testing for modern web apps | Playwright'

@pytest.mark.parametrize('execution_number', range(30))
def test_navigate_page(driver, execution_number):
    wait = WebDriverWait(driver, 30)
    action = ActionChains(driver)

    driver.implicitly_wait(5)
    driver.get("http://playwright.dev")

    el = driver.find_element(By.XPATH, '//*[@id="docusaurus_skipToContent_fallback"]/header/div/div/a')
    nav_bar_button = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div')

    wait.until(EC.element_to_be_clickable(el))
    el.click()

    wait.until(
        EC.staleness_of(nav_bar_button)
    )
    nav_bar_button = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div')

    wait.until(
        EC.url_to_be('https://playwright.dev/docs/intro')
    )

    wait.until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul'))
    )

    action.move_to_element(nav_bar_button).perform()

    wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul'))
    )

    el = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul/li[2]')
    el.click()

    wait.until(
        EC.url_to_be('https://playwright.dev/python/docs/intro')
    )

    el = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/a')
    assert el.get_attribute('innerText') == 'Python'

    el = driver.find_element(By.XPATH, '//*[@id="__docusaurus"]/nav/div[1]/div[2]/div[2]/button')
    el.click()

    el = driver.find_element(By.XPATH, '//*[@id="docsearch-input"]')
    el.send_keys('Getting Started')
    assert el.get_attribute('value') == 'Getting Started'

    el = driver.find_element(By.XPATH, '//*[@id="docsearch-list"]')
    el = el.find_element(By.XPATH, '//*[text()="Getting started - Library"]')

    wait.until(
        EC.visibility_of(el)
    )
    el.send_keys(Keys.ENTER)

    wait.until(
        EC.url_to_be('https://playwright.dev/python/docs/library')
    )
