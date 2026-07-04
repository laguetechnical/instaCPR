from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def performaction(driver):
    name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "173734026110493")
        )
    )

    name_input.clear()
    name_input.send_keys("its my own content")

    print("[+] copied content's description entered")