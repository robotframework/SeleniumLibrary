from selenium import webdriver


def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    return options
