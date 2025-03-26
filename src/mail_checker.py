import os
import imaplib
import logging
import sys
import re
import email
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "../config"))
from config import EMAIL_ADDRESS, PASSWORD, IMAP_SERVER, IMAP_PORT, SEARCH_CRITERIA

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


class MailChecker:
    def __init__(self):
        self.driver: webdriver.Chrome = self.__init_webdriver__()
        self.mail: imaplib.IMAP4_SSL = self.__init_mailbox__()

    def __del__(self):
        self.close()

    @staticmethod
    def __init_webdriver__() -> webdriver.Chrome:
        logging.info("Initializing WebDriver...")
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            logging.info("WebDriver initialized successfully.")
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {e}")
            logging.error("Ensure that Chrome WebDriver is installed and accessible.")
            print(
                "Critical Error: Failed to initialize WebDriver. Check logs for details."
            )
            return None

    @staticmethod
    def __init_mailbox__() -> imaplib.IMAP4_SSL:
        logging.info("Initializing IMAP mailbox...")
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, port=IMAP_PORT)
            mail.login(EMAIL_ADDRESS, PASSWORD)
            logging.info("IMAP mailbox initialized successfully.")
            return mail
        except Exception as e:
            logging.error(f"Failed to initialize IMAP mailbox: {e}")
            print(
                "Critical Error: Failed to initialize IMAP mailbox. Check logs for details."
            )
            return None

    def close(self) -> None:
        logging.info("Closing resources...")
        self.__close_webdriver__()
        self.__close_mailbox__()

    def __close_webdriver__(self) -> None:
        if hasattr(self, "driver") and self.driver:
            logging.info("Closing WebDriver...")
            self.driver.quit()
            logging.info("WebDriver closed.")

    def __close_mailbox__(self) -> None:
        if hasattr(self, "mail") and self.mail:
            logging.info("Closing IMAP connection...")
            try:
                self.mail.close()
                logging.info("IMAP connection closed.")
            except Exception as e:
                logging.warning(f"Error closing IMAP connection: {e}")

            try:
                self.mail.logout()
                logging.info("Logged out from IMAP.")
            except Exception as e:
                logging.warning(f"Error logging out from IMAP: {e}")

    def check_mail(self) -> str:
        try:
            self.mail.select("inbox")
            result, data = self.mail.search(None, f"{SEARCH_CRITERIA}")
            mail_ids = data[0].split()

            if not mail_ids:
                logging.info("No matching emails found")
                return ""

            latest_email_id = mail_ids[-1]
            status, msg_data = self.mail.fetch(latest_email_id, "(RFC822)")

            if status != "OK":
                logging.error("Failed to fetch email")
                return ""

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body_payload = part.get_payload(decode=True).decode()
                                break
                    else:
                        body_payload = msg.get_payload(decode=True).decode()

                    links = re.findall(
                        r"https?://[^\s<>\"\']+/account/update-primary-location.+",
                        body_payload,
                    )
                    return links[0] if links else ""

            return ""
        except Exception as e:
            logging.error(f"Error while checking mail: {e}")
            print("Error: Failed to check mail. Check logs for details.")
            return ""

    def click_button(self, link: str) -> bool:
        if not link:
            logging.error("Provided link is empty.")
            print("Error: Provided link is empty.")
            return False
        try:
            self.driver.get(link)
            time.sleep(2)
            button = self.driver.find_element(
                By.CSS_SELECTOR, '[role="button"][type="button"]'
            )
            button.click()
            print("Button clicked successfully.")
            return True
        except Exception as e:
            logging.error(f"Error while clicking button on {link}: {e}")
            print("Error: Failed to click button. Check logs for details.")
            return False
