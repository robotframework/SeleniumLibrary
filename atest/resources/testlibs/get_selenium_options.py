from selenium import webdriver


def get_chrome_options():
    options = webdriver.ChromeOptions()
    return options.add_argument('--disable-dev-shm-usage')
