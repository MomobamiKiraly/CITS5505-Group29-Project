from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create a known user before login-related tests
def ensure_test_user():
    from app import create_app, db
    from app.models import User
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username="seleniumuser").first()
        if not user:
            u = User(username="seleniumuser", email="seleniumuser@example.com")
            u.set_password("password")
            db.session.add(u)
            db.session.commit()

# Generate unique usernames to avoid duplication
def unique_name(prefix="user"):
    return f"{prefix}_{int(time.time())}"


def test_register_and_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")

    unique_username = unique_name("seleniumuser")

    # Fill step 1: basic user info
    driver.find_element(By.NAME, "username").send_keys(unique_username)
    driver.find_element(By.NAME, "email").send_keys(f"{unique_username}@example.com")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "confirm_password").send_keys("password")

    # Go to step 2
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "favorite_team")))

    # Fill hidden fields via JavaScript
    driver.execute_script("document.getElementById('favorite_team').value = 'Red Bull'")
    driver.execute_script("document.getElementById('favorite_driver').value = 'Max Verstappen'")

    # Submit form
    driver.find_element(By.NAME, "submit").click()

    # Check redirected to login
    WebDriverWait(driver, 5).until(EC.title_contains("Login"))
    assert "Login" in driver.title
    driver.quit()


def test_login_success():
    ensure_test_user()  # Make sure test user exists
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Fill login form
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
    ensure_test_user()
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Log in first
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    # Navigate to upload page
    driver.get("http://localhost:5000/upload")

    # Fill prediction text if available
    textareas = driver.find_elements(By.TAG_NAME, "textarea")
    if textareas:
        textareas[0].send_keys("Max Verstappen, Lando Norris, Charles Leclerc")
    driver.find_element(By.TAG_NAME, "form").submit()

    # Wait for profile page redirect
    WebDriverWait(driver, 5).until(EC.title_contains("Profile"))
    assert "Profile" in driver.title or "seleniumuser" in driver.page_source
    driver.quit()


def test_user_search():
    ensure_test_user()
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")

    # Log in
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    # Search for users
    driver.get("http://localhost:5000/search?q=selenium")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "ul")))

    assert "seleniumuser" in driver.page_source.lower()
    driver.quit()


def test_register_with_driver_selection():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/register")

    unique_username = unique_name("selenium_driver")
    unique_email = f"{unique_username}@example.com"

    # Fill step 1
    driver.find_element(By.NAME, "username").send_keys(unique_username)
    driver.find_element(By.NAME, "email").send_keys(unique_email)
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.NAME, "confirm_password").send_keys("password")
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()

    # Wait for teams to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "team")))
    teams = driver.find_elements(By.CLASS_NAME, "team")
    teams[0].click()

    # Wait and select a driver
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "driver")))
    drivers = driver.find_elements(By.CLASS_NAME, "driver")
    assert len(drivers) > 0
    drivers[0].click()

    # Ensure hidden fields were updated
    fav_team = driver.find_element(By.ID, "favorite_team").get_attribute("value")
    fav_driver = driver.find_element(By.ID, "favorite_driver").get_attribute("value")
    assert fav_team != ""
    assert fav_driver != ""

    # Submit registration form
    driver.find_element(By.NAME, "submit").click()

    # If already exists, skip assertion
    time.sleep(2)
    if "already exists" in driver.page_source:
        print("⚠️ Username/email already exists. Skipping assertion.")
        driver.quit()
        return

    WebDriverWait(driver, 5).until(EC.title_contains("Login"))
    assert "Login" in driver.title
    driver.quit()
    
    
def test_dashboard_renders_chart():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver = webdriver.Chrome()
    driver.get("http://localhost:5000/login")
    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 5).until(EC.url_contains("/dashboard"))

    # Check if chart image is rendered
    chart = driver.find_element(By.TAG_NAME, "img")
    assert "standings.png" in chart.get_attribute("src")
    driver.quit()