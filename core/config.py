import os
from dotenv import load_dotenv

load_dotenv()

# Form URLs
INSTAGRAM_FORM_URL = "https://help.instagram.com/contact/552695131608132"
FACEBOOK_FORM_URL = "https://www.facebook.com/help/contact/copyrightform"

DEFAULT_COUNTRY = "India"
DEFAULT_COPIED_TYPE = "Video"
OTP_TIMEOUT = 5  # seconds
SELENIUM_TIMEOUT = 60

# Paths
SCREENSHOT_DIR = "screenshots"
REPORT_DIR = "reports"
LOG_DIR = "logs"

# Headless mode (set via env for bot)
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"