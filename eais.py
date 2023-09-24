import os
import time
from pathlib import Path

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver: WebDriver, username: str, password: str) -> None:
    """Perform login to eais."""
    # Navigate to the given URL
    driver.get("https://www.eais.go.kr/moct/awp/abb01/AWPABB01F01")

    # Wait for the login form to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.loginForm"))
    )

    # Find the username and password fields and fill them
    driver.find_element(By.CSS_SELECTOR,
                        "div.loginForm input#membId").send_keys(username)
    driver.find_element(By.CSS_SELECTOR,
                        "div.loginForm input#pwd").send_keys(password)

    # Click the login button
    driver.find_element(By.CSS_SELECTOR,
                        "div.loginForm button.btnLogin").click()


def wait_loading(driver: WebDriver):
    """Wait until element "div.loadingWrap" disappears."""
    time.sleep(3)
    try:
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, "div.loadingModal")))
    except TimeoutException:
        print("Wait loading timeout")


def issue_registration(driver: WebDriver, address: str):
    """Issue a registration given building address.

    User should be already logged in.

    Args:
        driver: current web driver
        address: the street address of the building
    """
    # Go to the given URL
    driver.get("https://www.eais.go.kr/moct/bci/aaa02/BCIAAA02L01")

    # Wait for the address search button to be clickable and click it
    wait_loading(driver)
    button_address_search = driver.find_element(By.CSS_SELECTOR,
                                                "button.btnAddrSrch")
    button_address_search.click()

    # Wait until the pop-up is present
    div_pop_up = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.popAddrSearch")))

    # Fill in the address
    (div_pop_up.find_element(By.CSS_SELECTOR, "input#keyword")
     .send_keys(address))

    # Click the next button
    div_pop_up.find_element(By.CSS_SELECTOR, "button.btnNext").click()

    # Wait until the address list is present
    div_addr_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "div.popAddrSearch div.addrList")))

    # Click the first button in the address list
    div_addr_list.find_element(By.CSS_SELECTOR, "button").click()

    # Wait until the checkbox input is clickable and click it
    wait_loading(driver)
    checkbox_input = driver.find_element(By.CSS_SELECTOR,
                                         "input.ag-checkbox-input")
    checkbox_input.click()

    # Click the add to cart button
    button_add_cart = driver.find_element(By.CSS_SELECTOR,
                                          "button.btnAddCart")
    button_add_cart.click()

    # Click the submit button is clickable
    button_submit = driver.find_element(By.CSS_SELECTOR,
                                        "button.btnSubmit")
    button_submit.click()

    # Wait until the next button is clickable and click it
    wait_loading(driver)
    button_next = driver.find_element(By.CSS_SELECTOR, "button.btnNext")
    button_next.click()


def dowload_registration(driver: WebDriver, location: str):
    """Downloads pdf file of the last issued registration of a building.

    User should be already logged in.

    The desired building registration should be already issued.

    The pdf downloads in the user Downloads directory.
    The download file is named "report.pdf".
    If the file already exists the file is named "report (n).pdf",
    where `n` is an appropriate integer number to prevent name collision.

    Args:
        driver (webdriver): Instance of the browser's WebDriver.
        location (str): The land-lot number location of the building.
    """

    driver.get("https://www.eais.go.kr/moct/bci/aaa04/BCIAAA04L01")

    # Wait for the table to load and find the rows
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table.tableScroll tbody tr"))
    )

    # Loop over rows to find the one with the location in the 4th column
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        if cols[3].text == location:
            # When the location is found, click the link in the 5th column
            cols[4].find_element(By.CSS_SELECTOR, 'a.tbsBadge').click()
            break

    # Wait for new window to open and switch to it
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])

    # Find the print button and extract its onclick attribute
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button.report_menu_print_button_svg"))
    )
    onclick = button.get_attribute('onclick')

    # Modify the onclick string as required
    script_to_execute = onclick.split('.')[0] + ".pdfDownLoad()"

    # Execute the script
    driver.execute_script(script_to_execute)

    # Wait for download to finish.
    time.sleep(3)
    download_dir = str(Path.home() / "Downloads")
    WebDriverWait(driver, 60).until(lambda d: not any(
        [filename.endswith(".crdownload") for filename in
         os.listdir(download_dir)]))

    # Close the current window and switch back to the main window
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
