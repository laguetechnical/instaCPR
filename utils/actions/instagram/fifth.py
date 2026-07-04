from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

def performaction(driver,assertingcountry):
    country = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.ID, "1460192845847447")
        )
    )

    Select(country).select_by_value(assertingcountry)

    print("[+] Country selected:", assertingcountry)