from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys

# 1. Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://goexpense.bain.com/expense/#/app/not-submitted")

# 2. Manual login
input("🔐 Log in manually, then press Enter to continue...")

# 3. Click "New Item"
wait = WebDriverWait(driver, 20)
new_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New Item')]")))
new_item.click()
print("✅ Clicked 'New Item'")

time.sleep(2)  # Just to let row settle
date_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'DD-MMM')]")))
date_field.clear()
date_field.send_keys("07-Jun-2025")
print("✅ Date filled")
date_field.send_keys(Keys.TAB)

type_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
type_field.send_keys("Meals - Late/OT @ Home")
time.sleep(10)  # Just to let row settle
print("✅ Type filled")
type_field.send_keys(Keys.TAB)

case_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
case_field.send_keys("L7QC")
time.sleep(5)  # Just to let row settle
print("✅ Case filled")
case_field.send_keys(Keys.TAB)

filler_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
filler_field.send_keys(Keys.TAB)

amount_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
amount_field.send_keys("100")
time.sleep(2)  # Just to let row settle
print("✅ Amount filled")
amount_field.send_keys(Keys.TAB)

textarea = driver.find_element(By.NAME, "Reason for Late Work")
# textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='Required']")
textarea.send_keys("Case Work")
print("✅ Reason filled")


new_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New Item')]")))
new_item.click()
print("✅ Clicked 'New Item'")

time.sleep(2)  # Just to let row settle
date_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'DD-MMM')]")))
date_field.clear()
date_field.send_keys("08-Jun-2025")
print("✅ Date filled")
date_field.send_keys(Keys.TAB)

type_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
type_field.send_keys("Meals - Late/OT @ Home")
time.sleep(10)  # Just to let row settle
print("✅ Type filled")
type_field.send_keys(Keys.TAB)

case_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
case_field.send_keys("L7QC")
time.sleep(5)  # Just to let row settle
print("✅ Case filled")
case_field.send_keys(Keys.TAB)

filler_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
filler_field.send_keys(Keys.TAB)

amount_field = driver.switch_to.active_element
time.sleep(2)  # Just to let row settle
amount_field.send_keys("500")
time.sleep(2)  # Just to let row settle
print("✅ Amount filled")
amount_field.send_keys(Keys.TAB)

textarea = driver.find_elements(By.NAME, "Reason for Late Work")[1]
# textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='Required']")
textarea.send_keys("Case Work 2")
print("✅ Reason filled")

# Hold browser open for check
input("👀 Verify everything filled. Press Enter to close...")

driver.quit()