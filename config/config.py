import os
from dotenv import load_dotenv

load_dotenv("config/.env")

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')
IMAP_PORT = os.getenv('IMAP_PORT')
SEARCH_CRITERIA = os.getenv('SEARCH_CRITERIA')