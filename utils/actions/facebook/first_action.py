from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def performaction(driver):
    wait = WebDriverWait(driver, 20)

    radio = wait.until(
        EC.presence_of_element_located(
            (By.ID, "250116565117827.0")
        )
    )

    driver.execute_script("arguments[0].click();", radio)

    print("[+] Selected")