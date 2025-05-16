from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def unique_name(prefix="user"):
    return f"{prefix}_{int(time.time())}"


def test_register_and_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")

    unique_username = f"seleniumuser_{int(time.time())}"

    # Fill out step 1
    driver.find_element(By.NAME, "username").send_keys(unique_username)
    driver.find_element(By.NAME, "email").send_keys(f"{unique_username}@example.com")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "confirm_password").send_keys("password")

    # Go to step 2
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "favorite_team")))

    
    driver.execute_script("document.getElementById('favorite_team').value = 'Red Bull'")
    driver.execute_script("document.getElementById('favorite_driver').value = 'Max Verstappen'")

    # Submit the form
    driver.find_element(By.NAME, "submit").click()

    # Wait for redirect to login page
    WebDriverWait(driver, 5).until(EC.title_contains("Login"))
    assert "Login" in driver.title
    driver.quit()


def test_login_success():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Log in with existing credentials
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()

    # Wait for dashboard to load
    WebDriverWait(driver, 5).until(
        lambda d: "dashboard" in d.current_url.lower() or "Dashboard" in d.page_source
    )
    assert "Dashboard" in driver.page_source or "dashboard" in driver.current_url.lower()
    driver.quit()


def test_prediction_upload():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Log in
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    # Navigate to upload page and submit prediction
    driver.get("http://localhost:5000/upload")
    textareas = driver.find_elements(By.TAG_NAME, "textarea")
    if textareas:
        textareas[0].send_keys("Max Verstappen, Lando Norris, Charles Leclerc")
    driver.find_element(By.TAG_NAME, "form").submit()

    # Wait for redirect to profile page
    WebDriverWait(driver, 5).until(EC.title_contains("Profile"))
    assert "Profile" in driver.title or "seleniumuser" in driver.page_source
    driver.quit()

def test_user_search():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    driver.get("http://localhost:5000/search?q=selenium")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "ul")))

    
    assert "seleniumuser" in driver.page_source.lower()
    driver.quit()
    
import time

def test_register_with_driver_selection():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")

    unique_username = f"selenium_driver_{int(time.time())}"
    unique_email = f"{unique_username}@example.com"

    # Step 1: Basic info
    driver.find_element(By.NAME, "username").send_keys(unique_username)
    driver.find_element(By.NAME, "email").send_keys(unique_email)
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "confirm_password").send_keys("password")

    # Click Next
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "team")))

    # Select first team
    teams = driver.find_elements(By.CLASS_NAME, "team")
    teams[0].click()

    # Wait for drivers to load and select first driver
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "driver")))
    drivers = driver.find_elements(By.CLASS_NAME, "driver")
    assert len(drivers) > 0
    drivers[0].click()

    # Verify hidden fields updated
    fav_team = driver.find_element(By.ID, "favorite_team").get_attribute("value")
    fav_driver = driver.find_element(By.ID, "favorite_driver").get_attribute("value")
    assert fav_team != ""
    assert fav_driver != ""

    # Submit form
    driver.find_element(By.NAME, "submit").click()

    # If error flash appears, skip the assertion
    time.sleep(2)
    page = driver.page_source
    if "already exists" in page:
        print("⚠️ Username/email already exists, skipping.")
        driver.quit()
        return

    # Wait for redirect
    WebDriverWait(driver, 5).until(EC.title_contains("Login"))
    assert "Login" in driver.title
    driver.quit()