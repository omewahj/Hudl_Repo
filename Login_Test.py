from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import base64
import time

EMAIL_ID = "omewahjoel@gmail.com"


def hudl_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    wait = WebDriverWait(driver, 7)

    driver.maximize_window()

    # Assert that driver is on title page
    try:
        driver.get("https://www.hudl.com/")
        time.sleep(2)
        assert "We Help Teams and Athletes Win" in driver.title
        print("Home page loaded")
    except (AssertionError, WebDriverException):
        print("ERROR: Unable to reach home page")
        return

    try:
        # wait until Login in button is clickable and then click
        log_in_buttons = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div.outer > header > div > a.mainnav__btn.mainnav__btn--primary")))
        log_in_buttons.click()
        time.sleep(2)
        assert "Log In" in driver.title
        print('Home page log in button clicked successfully')
    except (AssertionError, TimeoutException):
        print('ERROR: Home page log in button un-clickable')
        return

    # wait until email input box is visible and enter username and encrypted password
    username_field = wait.until(EC.visibility_of_element_located((By.ID, "email")))


    username_field.send_keys(EMAIL_ID)

    with open('password.txt', 'r') as myfile:
        passwordVar = myfile.read().replace('\n', '')

    pwrd_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    pwrd_field.send_keys(base64.b64decode(passwordVar).decode("utf-8"))

    # Click main log in button
    main_log_in_button = wait.until(EC.visibility_of_element_located((By.ID, "logIn")))
    main_log_in_button.click()

    time.sleep(2)

    # Validate element found after logging in
    try:
        assert "Home - Hudl" in driver.title
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='ssr-webnav']/div/div[1]/nav[1]/div[4]/div[2]")))
        print('Successful Login Test')
    except (TimeoutException, AssertionError):
        print('ERROR: Unable to log in')
        try:
            # Check for invalid credentials
            wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/section/div[2]/div/form/div/div[3]")))
            print('ERROR: Invalid Credentials Error')
        except TimeoutException:
            return

    driver.quit()


if __name__ == '__main__':
    hudl_login()
