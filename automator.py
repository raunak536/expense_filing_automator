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
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import base64
from pdf2image import convert_from_bytes
import io
api_key = os.getenv("OPENAI_API_KEY")

def file_expense(expenses):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://goexpense.bain.com/expense/#/app/not-submitted") #Go expense website
    time.sleep(3)
    os.system('osascript login.scpt')
    client = OpenAI(api_key=api_key)

    # iterating through each row submitted in the app
    for row_enum, row in enumerate(expenses):
        # iterating through each bill uploaded in each row
        for file_enum, file in enumerate(row['files']):
            print(f"\nFiling row #{row_enum+1} and bill # {file_enum+1} ......................")
            # If bill uploaded in pdf; Assumes main bill is on first page of the PDF
            if file.content_type == "application/pdf":
                pages = convert_from_bytes(file.read())
                img_io = io.BytesIO()
                pages[0].save(img_io, format="JPEG")
                image_data = base64.b64encode(img_io.getvalue()).decode("utf-8")
            else:
                image_data = base64.b64encode(file.read()).decode("utf-8")
            # 2. Send it to GPT-4o
            response = client.responses.create(model="gpt-4o",
                                               input=[{"role": "user",
                                                       "content": [
                                                           {"type": "input_text",
                                                            "text": """Extract the total amount and the date from this receipt. 
                                                            Make sure to remove Rs or any other currency symbol from the amount extracted as I will later convert it to a float.
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

            amount = float(eval(response.output_text)['amount'])
            date = eval(response.output_text)['date']

            wait = WebDriverWait(driver, 20)
            
            # Generating new row
            try:
                new_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New Item')]")))
                new_item.click()
                time.sleep(3)  # Just to let row settle
            except Exception as e:
                print(f"Error while generating new row : {e}")

            # Filling in the date field
            try:
                date_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@placeholder, 'DD-MMM')]")))
                date_field.clear()
                date_field.send_keys(date)
                time.sleep(2)
                date_field.send_keys(Keys.TAB)
                time.sleep(3)
            except Exception as e:
                print(f"Error while filling in the date field : {e}")

            # Filling in the type field
            try:
                type_field = driver.switch_to.active_element
                type_field.send_keys(row['type'])
                time.sleep(10)  # Just to let row settle
                type_field.send_keys(Keys.TAB)
                time.sleep(5)  # Just to let row settle
            except Exception as e:
                print(f"Error while filling in the type field : {e}")
                
            # Filling in the case code
            try:
                case_field = driver.switch_to.active_element
                case_field.send_keys(row['case_code'])
                time.sleep(3)  # Just to let row settle
                case_field.send_keys(Keys.TAB)
                time.sleep(2)  # Just to let row settle
            except:
                print(f"Error while filling in the case code field : {e}")

            # Filling in the filler code
            try:
                filler_field = driver.switch_to.active_element
                filler_field.send_keys(Keys.TAB)
                time.sleep(2)  # Just to let row settle
            except:
                print(f"Error while filling in the empty filler field : {e}")
            
            # Filling in the amount
            try:
                amount_field = driver.switch_to.active_element
                time.sleep(3)  # Just to let row settle
                # amount_field.send_keys(min(amount,750))
                amount_field.send_keys(amount)
                time.sleep(3)  # Just to let row settle
                amount_field.send_keys(Keys.TAB)
                time.sleep(3)
            except:
                print(f"Error while filling in the amount field : {e}")
            
            # Filling in the reason
            try:
                if row['type'] == "Meals - Late/OT @ Client/Office":
                    textarea = driver.find_elements(By.NAME, "Reason for Late Work")
                elif row['type'] == "Meals - Business Travel":
                    textarea = driver.find_elements(By.NAME, "Explain Business Purpose")
                else:
                    raise Exception(f"Incorrect type of expense : {row['type']}")
                textarea[-1].send_keys(row['reason'])
                time.sleep(3)
            except:
                print(f"Error while filling in the reason field : {e}")

            # Uploading the bill
            try:
                driver.execute_script("window.scrollTo(0, 0);") # clicking at a random spot to deselect
                element = driver.find_element(By.XPATH, "//span[contains(text(), 'Expense Items')]")
                element.click()
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # clicking at a random spot to deselect
                file_input = driver.find_elements(By.XPATH, "//input[@ngf-select='grid.appScope.uploadReceipt($files, $invalidFiles,row.entity)']")
                # 2. Pass the temp path to Selenium for upload
                time.sleep(2)
                file_input[-1].send_keys(_save_temp_file(file))
                time.sleep(5)
                driver.execute_script("window.scrollTo(0, 0);") # clicking at a random spot to deselect
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # clicking at a random spot to deselect
            except:
                print(f"Error while uploading the bill : {e}")

            print(f"Done!")

    driver.quit()
    return

def _save_temp_file(filestorage):
    """Save any file (image/pdf/etc) to a temporary path and return the path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filestorage.filename)[1]) as tmp:
        filestorage.stream.seek(0)  # Always reset stream before read
        tmp.write(filestorage.read())
        return tmp.name

