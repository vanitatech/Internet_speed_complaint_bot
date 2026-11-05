
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os
from dotenv import load_dotenv


# Load login credentials from .env
load_dotenv()

Y_EMAIL = os.getenv("Y_EMAIL")
Y_PASSWORD = os.getenv("Y_PASSWORD")

# Promised internet speeds
PROMISED_DOWN = 1000
PROMISED_UP = 1000

Y_LOGIN_URL = "https://app.100daysofpython.dev/services/y/login"


class InternetSpeedYBot:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)

        self.down = 0
        self.up = 0

    def get_internet_speed(self):

        # Open Speedtest
        self.driver.get("https://www.speedtest.net/")

        # Reject cookies if the cookie banner appears
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.ID, "onetrust-reject-all-handler")
                )
            )
            cookie_button.click()

        except TimeoutException:
            pass

        # Click the Start button
        start_button = (
            By.CSS_SELECTOR,
            'button[aria-label="start speed test - connection type multi"]'
        )

        self.wait.until(
            EC.element_to_be_clickable(start_button)
        ).click()

        print("Speed test started...")

        # Wait for the results page
        WebDriverWait(self.driver, 180).until(
            EC.url_contains("/result/")
        )

        # Wait until download and upload speeds are displayed
        def speeds_ready(driver):
            elements = driver.find_elements(
                By.CSS_SELECTOR,
                "h3.font-mono.py-2.text-5xl"
            )

            if len(elements) >= 2 and all(
                element.text.strip() for element in elements[:2]
            ):
                return elements

            return False

        speed_elements = WebDriverWait(self.driver, 60).until(
            speeds_ready
        )

        # Extract download and upload speeds
        self.down = float(speed_elements[0].text)
        self.up = float(speed_elements[1].text)

        print(f"Download speed: {self.down} Mbps")
        print(f"Upload speed: {self.up} Mbps")

    def tweet_at_provider(self):

        # Only complain if speeds are below the promised speeds
        if self.down >= PROMISED_DOWN and self.up >= PROMISED_UP:
            print("Your internet speeds meet the promised speeds.")
            return

        # Open Y login page
        self.driver.get(Y_LOGIN_URL)

        # Enter email
        email = self.wait.until(
            EC.presence_of_element_located(
                (By.NAME, "email")
            )
        )
        email.send_keys(Y_EMAIL)

        # Enter password
        password = self.driver.find_element(
            By.NAME, "password"
        )
        password.send_keys(Y_PASSWORD)
        password.send_keys(Keys.ENTER)

        # Wait for the post text area
        post_box = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[aria-label="Post text"]')
            )
        )

        # Compose complaint
        tweet = (
            f"Hey Internet Provider, why is my speed "
            f"{self.down} Mbps down / {self.up} Mbps up "
            f"when I pay for {PROMISED_DOWN} Mbps down / "
            f"{PROMISED_UP} Mbps up?!"
        )

        post_box.click()
        post_box.send_keys(tweet)

        # Click the Post button
        post_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".x-compose-form button")
            )
        )

        post_button.click()

        print("Complaint posted successfully!")


# Run the bot
if __name__ == "__main__":

    if not Y_EMAIL or not Y_PASSWORD:
        raise ValueError(
            "Please set Y_EMAIL and Y_PASSWORD in your .env file."
        )

    bot = InternetSpeedYBot()

    try:
        bot.get_internet_speed()
        bot.tweet_at_provider()

    finally:
        bot.driver.quit()
