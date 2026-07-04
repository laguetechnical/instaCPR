from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def performaction(driver):
    submit = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[normalize-space()='Send']")
        )
    )

    driver.execute_script("arguments[0].click();", submit)

    print("[+] Submit clicked")