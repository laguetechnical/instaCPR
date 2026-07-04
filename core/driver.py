from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .exceptions import SeleniumActionError

class DriverManager:
    # Cache the service globally (initialized once)
    _service = None

    @classmethod
    def get_service(cls):
        if cls._service is None:
            print("[Driver] Initializing ChromeDriver (once)...")
            cls._service = Service(ChromeDriverManager().install())
        return cls._service

    def __init__(self, headless=False, proxy_address=None):
        self.headless = headless
        self.proxy_address = proxy_address
        self.driver = None

    def create(self):
        """Create driver with retries"""
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("detach", True)
        
        if self.proxy_address:
            options.add_argument(f"--proxy-server={self.proxy_address}")

        service = self.get_service()

        # Retry on startup failures
        for attempt in range(3):
            try:
                print(f"[Driver] Starting Chrome (attempt {attempt+1}/3)")
                self.driver = webdriver.Chrome(service=service, options=options)
                self.driver.maximize_window()
                print("[Driver] Chrome started successfully")
                return self.driver
            except Exception as e:
                print(f"[Driver] Attempt {attempt+1} failed: {e}")
                if attempt == 2:
                    raise
                time.sleep(3)

        raise Exception("Failed to start Chrome after 3 attempts")

    def retry(self, action, retries=3, delay=2):
        last_error = None
        for attempt in range(retries):
            try:
                return action()
            except Exception as e:
                last_error = e
                time.sleep(delay * (attempt + 1))
        raise SeleniumActionError(f"Action failed after {retries} retries: {last_error}")

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            finally:
                self.driver = None

    def screenshot(self, suffix="failure"):
        if not self.driver:
            return None
        Path("screenshots").mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path("screenshots") / f"{ts}_{suffix}.png"
        self.driver.save_screenshot(str(path))
        return str(path)