from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_register_and_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")

    # Fill out step 1
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "email").send_keys("selenium@example.com")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "confirm_password").send_keys("password")

    # Go to step 2
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "favorite_team")))

    # Manually assign values to hidden fields
    driver.execute_script("document.getElementById('favorite_team').value = 'Red Bull'")
    driver.execute_script("document.getElementById('favorite_driver').value = 'Max Verstappen'")

    # Submit the form
    driver.find_element(By.NAME, "submit").click()

    # Wait for redirect to login
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


def test_edit_profile():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Log in
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    # Navigate to edit profile page
    driver.get("http://localhost:5000/edit_profile")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "bio")))

    # Update bio
    bio_input = driver.find_element(By.NAME, "bio")
    bio_input.clear()
    bio_input.send_keys("Updated by Selenium test.")
    driver.find_element(By.TAG_NAME, "form").submit()

    time.sleep(2)
    assert "Profile" in driver.title or "updated" in driver.page_source.lower()
    driver.quit()


def test_friend_message():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Log in
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    # Go to friends page and open chat
    driver.get("http://localhost:5000/friends")
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-danger")))

    buttons = driver.find_elements(By.CLASS_NAME, "btn-danger")
    if buttons:
        driver.execute_script("arguments[0].click();", buttons[0])  # Force open modal
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "chatInput")))

        # Send a message
        msgbox = driver.find_element(By.ID, "chatInput")
        msgbox.send_keys("Hello from Selenium!")
        driver.find_element(By.ID, "sendBtn").click()
        time.sleep(2)
        assert "Hello" in driver.page_source
    driver.quit()