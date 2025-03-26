import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../config'))
from config import EMAIL_ADDRESS, PASSWORD, IMAP_SERVER, IMAP_PORT, SEARCH_CRITERIA
from mail_checker import MailChecker

class TestMailChecker(unittest.TestCase):
    
    @patch('mail_checker.webdriver.Chrome')
    @patch('mail_checker.imaplib.IMAP4_SSL')
    def setUp(self, mock_imap, mock_webdriver):
        self.mock_imap = mock_imap.return_value
        self.mock_webdriver = mock_webdriver
        self.mail_checker = MailChecker()

    def tearDown(self):
        self.mail_checker.close()
    
    def test_init_webdriver(self):
        self.assertIsNotNone(self.mail_checker.driver)
        self.mock_webdriver.assert_called_once()
    
    def test_init_mailbox(self):
        self.assertIsNotNone(self.mail_checker.mail)
        self.mock_imap.login.assert_called_once()
    
    @patch('mail_checker.email.message_from_bytes')
    def test_check_mail_success(self, mock_email_from_bytes):
        # Create a mock email message that simulates multipart structure
        mock_msg = MagicMock()
        mock_msg.is_multipart.return_value = True
        
        # Create a mock email part with the test link
        mock_part = MagicMock()
        mock_part.get_content_type.return_value = "text/plain"
        mock_part.get_payload.return_value = b'Click here: https://example.com/account/update-primary-location?token=123'
        mock_part.get_payload.side_effect = None
        
        # Set up the walk() method to yield our mock part
        mock_msg.walk.return_value = [mock_part]
        mock_email_from_bytes.return_value = mock_msg

        # Mock the IMAP responses
        self.mail_checker.mail.select.return_value = ('OK', [b'1'])
        self.mail_checker.mail.search.return_value = ('OK', [b'1'])
        self.mail_checker.mail.fetch.return_value = ('OK', [(b'1', (b'RFC822', b'email content'))])
        
        link = self.mail_checker.check_mail()
        self.assertEqual(link, 'https://example.com/account/update-primary-location?token=123')

    @patch('mail_checker.email.message_from_bytes')
    def test_check_mail_non_multipart(self, mock_email_from_bytes):
        # Create a mock email message that simulates non-multipart structure
        mock_msg = MagicMock()
        mock_msg.is_multipart.return_value = False
        mock_msg.get_payload.return_value = b'Click here: https://example.com/account/update-primary-location?token=456'
        mock_email_from_bytes.return_value = mock_msg

        # Mock the IMAP responses
        self.mail_checker.mail.select.return_value = ('OK', [b'1'])
        self.mail_checker.mail.search.return_value = ('OK', [b'1'])
        self.mail_checker.mail.fetch.return_value = ('OK', [(b'1', (b'RFC822', b'email content'))])
        
        link = self.mail_checker.check_mail()
        self.assertEqual(link, 'https://example.com/account/update-primary-location?token=456')

    @patch('mail_checker.email.message_from_bytes')
    def test_check_mail_no_link(self, mock_email_from_bytes):
        # Create a mock email message with no matching link
        mock_msg = MagicMock()
        mock_msg.is_multipart.return_value = False
        mock_msg.get_payload.return_value = b'No link in this email'
        mock_email_from_bytes.return_value = mock_msg

        self.mail_checker.mail.select.return_value = ('OK', [b'1'])
        self.mail_checker.mail.search.return_value = ('OK', [b'1'])
        self.mail_checker.mail.fetch.return_value = ('OK', [(b'1', (b'RFC822', b'email content'))])
        
        result = self.mail_checker.check_mail()
        self.assertEqual(result, '')  # Should return empty string when no link found
    
    def test_check_mail_no_email(self):
        self.mail_checker.mail.select.return_value = ('OK', [b'1'])
        self.mail_checker.mail.search.return_value = ('OK', [b''])  # Empty list of mail IDs
        result = self.mail_checker.check_mail()
        self.assertEqual(result, '')  # Should return empty string when no emails found
    
    def test_check_mail_fetch_failure(self):
        self.mail_checker.mail.select.return_value = ('OK', [b'1'])
        self.mail_checker.mail.search.return_value = ('OK', [b'1 2 3'])
        self.mail_checker.mail.fetch.return_value = ('NO', [None])
        link = self.mail_checker.check_mail()
        self.assertEqual(link, '')
    
    def test_click_button_success(self):
        self.mail_checker.driver.find_element.return_value.click.return_value = None
        result = self.mail_checker.click_button('https://example.com')
        self.assertTrue(result)
        self.mail_checker.driver.get.assert_called_once_with('https://example.com')
        self.mail_checker.driver.find_element.assert_called_once()
    
    def test_click_button_fail(self):
        self.mail_checker.driver.find_element.side_effect = Exception("Element not found")
        result = self.mail_checker.click_button('https://example.com')
        self.assertFalse(result)
    
    def test_close_webdriver(self):
        self.mail_checker.close()
        self.mail_checker.driver.quit.assert_called_once()
    
    def test_close_mailbox(self):
        self.mail_checker.close()
        self.mail_checker.mail.close.assert_called_once()
        self.mail_checker.mail.logout.assert_called_once()
    
    def test_init_webdriver_failure(self):
        with patch('mail_checker.webdriver.Chrome', side_effect=Exception("WebDriver Error")):
            checker = MailChecker()
            self.assertIsNone(checker.driver)
    
    def test_init_mailbox_failure(self):
        with patch('mail_checker.imaplib.IMAP4_SSL', side_effect=Exception("IMAP Error")):
            checker = MailChecker()
            self.assertIsNone(checker.mail)
    
    def test_mailbox_login_failure(self):
        self.mail_checker.mail.login.side_effect = Exception("Login failed")
        with self.assertRaises(Exception):
            self.mail_checker.mail.login('test@example.com', 'wrongpassword')

if __name__ == '__main__':
    unittest.main()