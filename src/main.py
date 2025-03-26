import time
from mail_checker import MailChecker

if __name__ == "__main__":
    while True:
        mail_checker = MailChecker()
        try:
            mail_checker.click_button(mail_checker.check_mail())
        finally:
            mail_checker.close()
        time.sleep(20)
