from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def performaction(driver,target_contenttext):
    name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "451242651624945")
        )
    )

    name_input.clear()
    name_input.send_keys(target_contenttext)

    print("[+] Name entered")