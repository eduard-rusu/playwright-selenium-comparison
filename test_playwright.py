import time
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(autouse=True)
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        yield browser.new_context(no_viewport=True)
        browser.close()


def test_has_title(browser):
    page = browser.new_page()
    page.goto("http://playwright.dev")
    assert page.title() == 'Fast and reliable end-to-end testing for modern web apps | Playwright'


def test_navigate_page(browser):
    page = browser.new_page()
    page.goto("http://playwright.dev")

    el = page.locator('xpath=//*[@id="docusaurus_skipToContent_fallback"]/header/div/div/a')
    el.click()

    page.wait_for_url('https://playwright.dev/docs/intro')
    el = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul')
    computed_style = el.evaluate("el =>  window.getComputedStyle(el)", el)
    assert computed_style['visibility'] == 'hidden'

    page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div').hover()
    el = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul')
    computed_style = el.evaluate("el =>  window.getComputedStyle(el)", el)
    assert computed_style['visibility'] == 'visible'

    page.click('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/ul/li[2]')
    page.wait_for_url('https://playwright.dev/python/docs/intro')

    el = page.locator('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[1]/div/a')
    assert el.inner_text() == 'Python'

    # Click on search button
    page.click('xpath=//*[@id="__docusaurus"]/nav/div[1]/div[2]/div[2]/button')
    page.fill('xpath=//*[@id="docsearch-input"]', 'Getting Started')

    el = page.locator('//*[@id="docsearch-list"]').get_by_text('Getting started - Library')
    el.wait_for(state='visible')
    page.keyboard.press('Enter')

    page.wait_for_url('https://playwright.dev/python/docs/library')