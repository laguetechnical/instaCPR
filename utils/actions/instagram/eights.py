from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def performaction(driver,copied_contenturl):
    name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "1345014673172459")
        )
    )

    name_input.clear()
    name_input.send_keys(copied_contenturl)

    print("[+] copied content url link entered")