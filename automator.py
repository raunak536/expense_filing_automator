from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import os
from PIL import Image
import tempfile
# 1. Setup

# input("✅ Logged in? Press Enter to continue automation...")
# 2. Manual login
# input("🔐 Log in manually, then press Enter to continue...")


from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import base64

def file_expense(expenses):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://goexpense.bain.com/expense/#/app/not-submitted")
    time.sleep(3)
    os.system('osascript login.scpt')
    client = OpenAI()

    # 1. Read and encode the image
    # with open("/Users/72625/Documents/general/expense_filing_automator/uploads/13jan_223.jpeg", "rb") as image_file:
    #     image_data = base64.b64encode(image_file.read()).decode("utf-8")
    for row in expenses:
        for file in row['files']:
            image_data = base64.b64encode(file.read()).decode("utf-8")
            # 2. Send it to GPT-4o
            response = client.responses.create(model="gpt-4o",
                                               input=[{"role": "user",
                                                       "content": [
                                                           {"type": "input_text",
                                                            "text": """Extract the total amount and the date from this receipt. 
                                                                    Respond **only** with a dict object so that I can directly use the output.
                                                                    Format of dictionary :
            
            {
              "amount": "amount",
              "date": "date"
            }
            NOTE 1 : Respond ONLY with a JSON object (no Markdown block, no explanation). Do NOT wrap the JSON in ```. 
            NOTE 2: 'date' should be in this format %d-%b-%Y"""},
                                                           {"type": "input_image",
                                                            "image_url": f"data:image/jpeg;base64,{image_data}"},
                        ],
                    }
                ],
            )

            # 3. Print response
            # print(response.output_text)

            amount = float(eval(response.output_text)['amount'])
            date = eval(response.output_text)['date']

            # 3. Click "New Item"
            wait = WebDriverWait(driver, 20)
            new_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New Item')]")))
            new_item.click()
            print("✅ Clicked 'New Item'")

            time.sleep(3)  # Just to let row settle
            date_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'DD-MMM')]")))
            date_field.clear()
            date_field.send_keys(date)
            time.sleep(2)
            print("✅ Date filled")
            date_field.send_keys(Keys.TAB)
            time.sleep(3)
            type_field = driver.switch_to.active_element
            type_field.send_keys(row['type'])
            time.sleep(8)  # Just to let row settle
            print("✅ Type filled")
            type_field.send_keys(Keys.TAB)
            time.sleep(2)  # Just to let row settle
            case_field = driver.switch_to.active_element
            case_field.send_keys(row['case_code'])
            time.sleep(3)  # Just to let row settle
            print("✅ Case filled")
            case_field.send_keys(Keys.TAB)
            time.sleep(2)  # Just to let row settle
            filler_field = driver.switch_to.active_element
            filler_field.send_keys(Keys.TAB)
            time.sleep(2)  # Just to let row settle
            amount_field = driver.switch_to.active_element
            time.sleep(3)  # Just to let row settle
            amount_field.send_keys(min(amount,750))
            time.sleep(3)  # Just to let row settle
            print("✅ Amount filled")
            amount_field.send_keys(Keys.TAB)
            time.sleep(3)
            if row['type'] == "Meals - Late/OT @ Home":
                textarea = driver.find_elements(By.NAME, "Reason for Late Work")
            else:
                textarea = driver.find_elements(By.NAME, "Explain Business Purpose")
            # textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='Required']")
            textarea[-1].send_keys(row['reason'])
            print("✅ Reason filled")
            time.sleep(3)
            # driver.find_elements(By.TAG_NAME, "body")[0].click()
            driver.execute_script("window.scrollTo(0, 0);")
            element = driver.find_element(By.XPATH, "//span[contains(text(), 'Expense Items')]")
            element.click()
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            file_input = driver.find_elements(By.XPATH, "//input[@ngf-select='grid.appScope.uploadReceipt($files, $invalidFiles,row.entity)']")
            # 2. Pass the temp path to Selenium for upload
            time.sleep(2)
            file_input[-1].send_keys(convert_to_jpeg(file))
            time.sleep(5)
        # file_input.send_keys("/Users/72625/Documents/general/expense_filing_automator/uploads/13jan_223.jpeg")

    # input("👀 Verify everything filled. Press Enter to close...")

    driver.quit()
    return

def convert_to_jpeg(filestorage):
    # 1. Read file as image
    try:
        image = Image.open(filestorage.stream).convert("RGB")
    except Exception as e:
        raise ValueError(f"Failed to open image: {filestorage.filename}, {e}")

    # 2. Create a temp JPEG path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg") as tmp:
        jpeg_path = tmp.name
        image.save(jpeg_path, format="JPEG")

    return jpeg_path
#
# new_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New Item')]")))
# new_item.click()
# print("✅ Clicked 'New Item'")
#
# time.sleep(2)  # Just to let row settle
# date_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'DD-MMM')]")))
# date_field.clear()
# date_field.send_keys("08-Jun-2025")
# time.sleep(2)
# print("✅ Date filled")
# date_field.send_keys(Keys.TAB)
#
# type_field = driver.switch_to.active_element
# time.sleep(5)  # Just to let row settle
# type_field.send_keys("Meals - Late/OT @ Home")
# time.sleep(10)  # Just to let row settle
# print("✅ Type filled")
# type_field.send_keys(Keys.TAB)
#
# case_field = driver.switch_to.active_element
# time.sleep(2)  # Just to let row settle
# case_field.send_keys("L7QC")
# time.sleep(5)  # Just to let row settle
# print("✅ Case filled")
# case_field.send_keys(Keys.TAB)
#
# filler_field = driver.switch_to.active_element
# time.sleep(2)  # Just to let row settle
# filler_field.send_keys(Keys.TAB)
#
# amount_field = driver.switch_to.active_element
# time.sleep(2)  # Just to let row settle
# amount_field.send_keys("500")
# time.sleep(2)  # Just to let row settle
# print("✅ Amount filled")
# amount_field.send_keys(Keys.TAB)
#
# textarea = driver.find_elements(By.NAME, "Reason for Late Work")[1]
# # textarea = driver.find_element(By.XPATH, "//textarea[@placeholder='Required']")
# textarea.send_keys("Case Work 2")
# print("✅ Reason filled")
#
# file_input = driver.find_elements(By.XPATH, "//input[@ngf-select='grid.appScope.uploadReceipt($files, $invalidFiles,row.entity)']")
# file_input[-1].send_keys("/Users/72625/Documents/general/expense_filing_automator/uploads/dec11-3.jpeg")

# Hold browser open for check
