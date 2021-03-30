import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Dashboard
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible(
                (By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector

        sub_measure()

    measure()


def export_dashboard_to_pdf(webdriver, datasets):
    # logging.info("datasets: %s", pformat(datasets))

    dashboard_page = Dashboard(webdriver)
    dashboard_page.page_url += "?selectPageId=10100"
    dashboard_page.go_to()

    def gadgets_are_loaded(driver):
        gadgets = driver.find_elements(By.CSS_SELECTOR, ".qrf-gadget[data-qrf-gadget-type]")
        for gadget in gadgets:
            if 'qrf-loading' in gadget.get_attribute("class"):
                return False
        return gadgets

    gadgets = WebDriverWait(webdriver, 30).until(gadgets_are_loaded)

    logging.info('Gadget types: %s', [g.get_attribute("data-qrf-gadget-type") for g in gadgets])

    def close_all_flags():
        flags = webdriver.find_elements(By.CSS_SELECTOR, ".aui-flag .aui-close-button")
        for flag in flags:
            WebDriverWait(webdriver, 10).until(lambda d: flag if flag.is_enabled() else False)
            flag.click()

    close_all_flags()

    export_button = WebDriverWait(webdriver, 10).until(
        EC.element_to_be_clickable((By.ID, "qrf-dashboard-export-button")))

    @print_timing("selenium_rf_pdf_export_dashboard")
    def measure():
        export_button.click()

        submit = WebDriverWait(webdriver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#qrf-dashboard-export-options-dialog .qrf-dialog-submit ")))

        submit.click()

        download = WebDriverWait(webdriver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.qrf-dashboard-export-save-link")))

        filename = download.get_attribute("download")

        logging.info('Downloaded filename: %s', filename)

    measure()
