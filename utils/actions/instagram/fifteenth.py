from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def performaction(driver):
    confirm = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Confirm']")
        )
    )

    driver.execute_script("arguments[0].click();", confirm)

    print("[+] Confirm clicked")