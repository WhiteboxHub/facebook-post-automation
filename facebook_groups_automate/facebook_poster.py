from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils import human_delay, log

class FacebookPoster:
    def __init__(self, email, password, headless=False):
        self.email = email
        self.password = password
        options = webdriver.ChromeOptions()
        if not headless:
            options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self):
        log("Navigating to Facebook login page.")
        self.driver.get("https://www.facebook.com/login")
        human_delay()
        self.driver.find_element(By.ID, "email").send_keys(self.email)
        human_delay(1, 2)
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        human_delay(1, 2)
        self.driver.find_element(By.NAME, "login").click()
        human_delay(5, 8)
        log("Logged in to Facebook.")

    def post_to_group(self, group_url, message):
        log(f"Navigating to group: {group_url}")
        self.driver.get(group_url)
        human_delay(5, 8)
        try:
            post_box = self.driver.find_element(By.XPATH, "//div[@aria-label='Create a public post…' or @aria-label='Create a post']")
            post_box.click()
            human_delay(2, 4)
            active_box = self.driver.switch_to.active_element
            active_box.send_keys(message)
            human_delay(2, 4)
            post_button = self.driver.find_element(By.XPATH, "//div[@aria-label='Post']")
            post_button.click()
            log(f"Posted to group: {group_url}")
            human_delay(5, 8)
        except Exception as e:
            log(f"Failed to post in {group_url}: {e}")

    def close(self):
        self.driver.quit()
        log("Closed browser.") 