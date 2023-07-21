import random
import time

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS
from selenium_ui.jira.pages.pages import Issue
from selenium.webdriver.common.keys import Keys

def app_specific_action(webdriver, datasets):
    issue_page = Issue(webdriver, issue_key=datasets['issue_key'])
    issue_page.go_to()
    issue_page.wait_for_page_loaded()

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        issue_page.wait_until_visible((By.ID, "wrap-labels"))
        label_name = BasePage.generate_random_string(6).replace(" ", "_")

        @print_timing("selenium_app_custom_action:create_label")
        def sub_measure():
            labels = issue_page.get_element((By.ID, "wrap-labels"))
            issue_page.action_chains().move_to_element(labels)
            issue_page.wait_until_visible((By.CSS_SELECTOR, "#wrap-labels > div > span")).click()
            issue_page.action_chains().send_keys(label_name).perform()
            issue_page.wait_until_visible((By.CSS_SELECTOR, "#jira > div.ajs-layer.box-shadow.active")).click()
            issue_page.wait_until_visible((By.CSS_SELECTOR, "#labels-form > div.save-options > button.aui-button.submit")).click()
            issue_page.wait_until_visible((By.CLASS_NAME, "labels"))

        sub_measure()

        @print_timing("selenium_app_custom_action:add_color")
        def sub_measure():
            labels = issue_page.get_element((By.XPATH, "//div[@id='wrap-labels']//a[.//span[contains(text(), '" + label_name + "')]]"))
            issue_page.action_chains().move_to_element(labels).perform()
            issue_page.wait_until_visible((By.XPATH, "//*[@id='lble-colorPicker']/table/tbody/tr[1]/td[1]/div")).click()
            time.sleep(2)
        sub_measure()

        issue_page.go_to()
        issue_page.wait_for_page_loaded()

        @print_timing("selenium_app_custom_action:validate_color")
        def sub_measure():
            issue_page.wait_until_visible((By.CLASS_NAME, "labels"))
            labels = issue_page.get_element((By.XPATH, "//div[@id='wrap-labels']//a[.//span[contains(text(), '" + label_name + "')]]"))
            print(labels.value_of_css_property("background-color"))
            assert labels.value_of_css_property("background-color") == "rgba(207, 159, 255, 1)"
        sub_measure()
    measure()

