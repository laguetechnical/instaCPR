from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def performaction(driver,otpnumb):
    name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div[2]/div[2]/div/input")
        )
    )
    name_input.clear()
    name_input.send_keys(otpnumb)

    print("[+] Name entered")