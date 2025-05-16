from selenium import webdriver
import time

def test_register_and_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")

    driver.find_element("name", "username").send_keys("testuser")
    driver.find_element("name", "email").send_keys("test@example.com")
    driver.find_element("name", "password").send_keys("password")
    driver.find_element("name", "confirm").send_keys("password")
    driver.find_element("tag name", "form").submit()

    time.sleep(2)
    assert "Login" in driver.page_source
    driver.quit()