# Web Scraping of the Korean Architectural Administration Information System (eais.go.kr)

The application is written in Python using Selenium.

All the functions are implemented in the Python module `eais`.

## Log in the Korean EAIS

Python scraping function using Selenium to perform login to EAIS:

```text
def login(driver: WebDriver, username: str, password: str):
    """Perform login to eais."""
    Go to url "https://www.eais.go.kr/moct/awp/abb01/AWPABB01F01"
    Wait until presence of element "div.loginForm"
    Fill in "input#membId" with `username`
    Fill in "input#pwd" with `password`
    Click "button.btnLogin"
```

## Issue Registration of a Building

Python scraping function using Selenium to issue the registration of a building, given its street address:

```text
def issue_registration(driver: WebDriver, address: str):
    """Issue a registration given building address.

    Args:
        driver: current web driver
        address: the street address of the building
    """
    Go to url "https://www.eais.go.kr/moct/bci/aaa02/BCIAAA02L01"
    Click "button.btnAddrSrch"
    Wait until presence of element "div.popAddrSearch"
    Fill in "div.popAddrSearch input#keyword" with the address
    Click "div.popAddrSearch button.btnNext"
    Wait until presence of element "div.popAddrSearch div.addrList"
    Click "div.popAddrSearch div.addrList button"
    Wait until presence of element "input.ag-checkbox-input"
    Check "input.ag-checkbox-input"
    Click "button.btnAddCart"
    Click "button.btnSubmit"
    Click "button.btnNext"
```

## Download an Issued Registration

The registrations issued go to user's list of issued registrations.

The following function downloads one of the registrations from the list as a PDF file. 

```text
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
    Go to url "https://www.eais.go.kr/moct/bci/aaa04/BCIAAA04L01"
    Find the first row of "table.tableScroll" where `location` appears on the 4th column
    On this row, click "a.tbsBadge" on the 5th column
    The registration report will be opened in a new browser window, wait for this window to open 
    Switch to the new window
    Find element "button.report_menu_print_button_svg"
    onclick = button "onclick" attribute
    Execute script: onclick start to the first "." inclusive + "pdfDownLoad()"
    wait for the download successed
    Close window and switch back to the first window

```

## Main Program

To demonstrate the use of the above functions, we build the main program that logs in the service and downloads the user's last issued registration of the building located in the given location.

```python
from selenium import webdriver

import eais

CHROME_OPTIONS = ["--start-maximized"]
USERNAME = "susumu1964"
PASSWORD = "sus3141592"
LOCATION = "경기도 고양시 일산동구 마두동 796"


def main():
    options = webdriver.ChromeOptions()
    for a in CHROME_OPTIONS:
        options.add_argument(a)
    with webdriver.Chrome(options) as driver:
        eais.login(driver, USERNAME, PASSWORD)
        eais.dowload_registration(driver, LOCATION)


if __name__ == "__main__":
    main()
```
