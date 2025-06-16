from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils import human_delay, log
import random
import time

class FacebookPoster:
    def __init__(self, email, password, headless=False):
        self.email = email
        self.password = password
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        
        # Enhanced anti-detection measures
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Add random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 30)  # Increased timeout
        
        # Add random mouse movements and scrolling
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def wait_for_captcha(self):
        """Wait for user to solve CAPTCHA manually"""
        log("CAPTCHA detected. Please solve it manually...")
        try:
            # Wait for either successful login or CAPTCHA
            self.wait.until(lambda driver: 
                len(driver.find_elements(By.XPATH, "//div[@aria-label='Account controls and settings']")) > 0 or
                len(driver.find_elements(By.XPATH, "//div[contains(@class, 'captcha')]")) > 0
            )
            
            # If CAPTCHA is present, wait for user to solve it
            if len(self.driver.find_elements(By.XPATH, "//div[contains(@class, 'captcha')]")) > 0:
                log("Waiting for CAPTCHA to be solved...")
                # Wait for successful login after CAPTCHA
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Account controls and settings']")))
                log("CAPTCHA solved successfully!")
                human_delay(3, 5)
        except Exception as e:
            log(f"Error while waiting for CAPTCHA: {str(e)}")
            raise

    def login(self):
        try:
            log("Navigating to Facebook login page.")
            self.driver.get("https://www.facebook.com/login")
            human_delay(3, 5)
            
            # Simulate human-like behavior
            self.simulate_human_behavior()
            
            # Wait for and fill email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            self.type_like_human(email_field, self.email)
            human_delay(1, 2)
            
            # Wait for and fill password
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, "pass")))
            self.type_like_human(password_field, self.password)
            human_delay(1, 2)
            
            # Click login and wait for navigation
            login_button = self.wait.until(EC.element_to_be_clickable((By.NAME, "login")))
            login_button.click()
            
            # Check for CAPTCHA
            self.wait_for_captcha()
            
            log("Successfully logged in to Facebook.")
            human_delay(3, 5)
            
        except Exception as e:
            log(f"Login failed: {str(e)}")
            raise

    def type_like_human(self, element, text):
        """Type text with random delays between keystrokes"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    def simulate_human_behavior(self):
        """Simulate human-like behavior with random mouse movements and scrolling"""
        try:
            # Random scroll
            scroll_amount = random.randint(100, 300)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            human_delay(0.5, 1)
            
            # Random mouse movement simulation
            self.driver.execute_script("""
                var event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': arguments[0],
                    'clientY': arguments[1]
                });
                document.dispatchEvent(event);
            """, random.randint(100, 700), random.randint(100, 500))
            
            human_delay(0.5, 1)
        except Exception as e:
            log(f"Error in human behavior simulation: {str(e)}")

    def follow_group(self, group_url):
        try:
            log(f"Checking if we need to follow group: {group_url}")
            self.driver.get(group_url)
            human_delay(3, 5)
            
            # Simulate human behavior before checking follow button
            self.simulate_human_behavior()
            
            # Look for follow button
            follow_buttons = self.driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'Follow')]")
            if follow_buttons:
                follow_button = follow_buttons[0]
                if "Follow" in follow_button.get_attribute("aria-label"):
                    log("Following the group...")
                    follow_button.click()
                    human_delay(2, 4)
                    return True
            return False
            
        except Exception as e:
            log(f"Error while trying to follow group: {str(e)}")
            return False

    def post_to_group(self, group_url, message, image_path=None):
        try:
            log(f"Navigating to group: {group_url}")
            self.driver.get(group_url)
            human_delay(5, 8)
            
            # Simulate human behavior
            self.simulate_human_behavior()
            
            # First ensure we're following the group
            self.follow_group(group_url)
            
            # Wait for the page to fully load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            human_delay(3, 5)
            
            # Wait for any overlays to disappear
            try:
                self.wait.until(EC.invisibility_of_element_located((
                    By.XPATH, "//ul[contains(@class, 'xuk3077')]"
                )))
            except:
                pass  # Ignore if no overlay is present
            
            # Find the write box using multiple approaches
            write_box = None
            write_box_selectors = [
                "//div[contains(@class, 'xi81zsa')]//span[contains(text(), 'Write something')]",
                "//span[contains(text(), 'Write something')]",
                "//div[contains(@class, 'x1lkfr7t')]//span[contains(text(), 'Write something')]"
            ]
            
            for selector in write_box_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            write_box = element
                            break
                    if write_box:
                        break
                except:
                    continue
            
            if not write_box:
                raise Exception("Could not find write box")
            
            # Scroll to the write box
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", write_box)
            human_delay(2, 4)
            
            # Try multiple ways to click the write box
            try:
                # Method 1: Regular click
                write_box.click()
            except:
                try:
                    # Method 2: JavaScript click
                    self.driver.execute_script("arguments[0].click();", write_box)
                except:
                    try:
                        # Method 3: Actions click
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(self.driver).move_to_element(write_box).click().perform()
                    except:
                        raise Exception("Could not click write box")
            
            human_delay(2, 4)
            
            # Wait for the post input field and type message
            post_input = self.wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[@role='textbox' or @contenteditable='true']"
            )))
            self.type_like_human(post_input, message)
            human_delay(2, 4)

            # Handle file upload if provided
            if image_path:
                try:
                    # Click "Add to your post"
                    add_to_post = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//div[@aria-label='Add to your post']"
                    )))
                    self.driver.execute_script("arguments[0].click();", add_to_post)
                    human_delay(2, 4)

                    # Step 1: Click the File option
                    file_option = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//span[contains(text(), 'File')]"
                    )))
                    self.driver.execute_script("arguments[0].click();", file_option)
                    human_delay(2, 4)

                    # Step 2: Click "Choose File" in the modal
                    choose_file = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//span[contains(text(), 'Choose File')]"
                    )))
                    self.driver.execute_script("arguments[0].click();", choose_file)
                    human_delay(2, 4)

                    # Step 3: Upload file
                    file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
                    file_input = None
                    for fi in file_inputs:
                        if fi.is_displayed():
                            file_input = fi
                            break
                    if not file_input:
                        raise Exception("No visible file input found")
                    file_input.send_keys(image_path)
                    log(f"Uploading file: {image_path}")
                    human_delay(5, 8)

                    # Step 4: Click Post button inside the file modal
                    post_button = self.wait.until(EC.element_to_be_clickable((
                        By.XPATH, "//span[contains(text(), 'Post')]/ancestor::div[@role='none']"
                    )))
                    self.driver.execute_script("arguments[0].click();", post_button)
                    log(f"Successfully posted to group: {group_url}")
                    human_delay(8, 12)

                except Exception as e:
                    log(f"Error uploading file: {str(e)}")
                    raise

            # Wait for any overlays to disappear before clicking post
            try:
                self.wait.until(EC.invisibility_of_element_located((
                    By.XPATH, "//ul[contains(@class, 'xuk3077')]"
                )))
            except:
                pass

            # Click post button using JavaScript
            post_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//div[@aria-label='Post']"
            )))
            self.driver.execute_script("arguments[0].click();", post_button)
            log(f"Successfully posted to group: {group_url}")
            human_delay(8, 12)
            
        except Exception as e:
            log(f"Failed to post in {group_url}: {str(e)}")
            raise

    def close(self):
        try:
            self.driver.quit()
            log("Browser closed successfully.")
        except Exception as e:
            log(f"Error while closing browser: {str(e)}") 