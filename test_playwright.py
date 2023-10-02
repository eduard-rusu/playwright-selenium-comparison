import time
import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

@pytest.fixture(autouse=True)
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--start-maximized'], channel='chrome')
        yield browser.new_context(no_viewport=True)
        browser.close()


#def test_has_title(browser):
#   page = browser.new_page()
#   page.goto("http://playwright.dev")
#   assert page.title() == 'Fast and reliable end-to-end testing for modern web apps | Playwright'


@pytest.mark.parametrize('execution_number', range(30))
def test_navigate_page(browser, execution_number):
    page = browser.new_page()
    page.goto("http://playwright.dev")

    nav_bar_button = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div')
    el = page.locator('xpath=//*[@id="docusaurus_skipToContent_fallback"]/header/div/div/a')
    el.click()

    page.wait_for_url('https://playwright.dev/docs/intro')

    el = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul')
    expect(el).to_be_hidden()

    nav_bar_button.wait_for(state='visible')
    nav_bar_button.hover()
    el = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul')
    el.wait_for(state="visible")

    page.click('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul/li[2]')
    page.wait_for_url('https://playwright.dev/python/docs/intro')

    el = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/a')
    expect(el).to_contain_text('Python')

    # Click on search button
    page.click('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[2]/div[2]/button')

    el = page.locator('xpath=//*[@id="docsearch-input"]')
    el.wait_for(state='visible')
    page.fill('xpath=//*[@id="docsearch-input"]', 'Getting Started')
    expect(el).to_have_value('Getting Started')

    el = page.locator('//*[@id="docsearch-list"]').get_by_text('Getting started - Library')
    el.wait_for(state='visible')
    page.keyboard.press('Enter')

    page.wait_for_url('https://playwright.dev/python/docs/library')
