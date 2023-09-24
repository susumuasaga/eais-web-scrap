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
