from selenium import webdriver
from selenium.webdriver import FirefoxOptions

# opts = FirefoxOptions()
# opts.add_argument("--headless")
# browser = webdriver.Firefox(options=opts)
browser = webdriver.Chrome()
browser.get('http://localhost:8000')

assert 'The install worked successfully! Congratulations!' in browser.title