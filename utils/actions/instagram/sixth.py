from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

def performaction(driver,copied_contenttype):
    CcT = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "418475341579315")
        )
    )

    Select(CcT).select_by_value(copied_contenttype)

    print("[+] Copied Content Type selected:", copied_contenttype)