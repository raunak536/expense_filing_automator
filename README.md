---

# AutoExpense: Automated Expense Filing with GPT-4o + Selenium

AutoExpense is a local web application that automates the process of filing expenses on the GoExpense platform.

Using a Flask backend + JS frontend, OpenAI’s GPT-4o for reading receipt images (including PDFs, PNGs, JPEGs), and Selenium to control Chrome, it simplifies expense submission into a drag-and-drop experience.

You fill in the form, upload your receipts, click **File Expense**, and the app takes care of the rest — including logging into GoExpense and filling out the form automatically through your browser.

---

## Features
- Upload multiple bills per expense row  
- Automatically extract and parse receipt data  
- Supports both image files (JPG, PNG) and PDFs (auto-converted)  
- Uses OpenAI API to intelligently extract dates and amounts  
- Securely caches GoExpense credentials during session  
- Files expenses using actual Chrome browser via Selenium  
- Fully offline after start (your data stays on your machine)  

▶ [Watch the walkthrough video](https://youtu.be/SbP1NK1FU4o)

---

## How to Use

### Step 1: Clone the github repo

Run in terminal : 
```bash
git clone https://github.com/raunak536/expense_filing_automator.git
cd expense_filing_automator
```

---

### Step 2: Create python env, install packages, store openai key

Run in terminal : 
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo 'OPENAI_API_KEY="insert_your_key_here"' > .env
```
---

### Step 3: Run the app and open it in Your Browser

Run in terminal : 
```bash
python app.py
```

Go to:
```
http://127.0.0.1:5001
```

---

### Step 4: Fill the Expense Form

- Each row = one expense item  
- Each row can take multiple bills, as long as case code and type are the same  

---

### Step 5: Click “File Expense”

- You’ll be prompted to enter your GoExpense credentials  
- These are cached for your session only (not stored permanently)  

---

### Step 6: Let the Bot Do Its Thing 

- The app will open Chrome and file your expenses automatically  
- **Do not use the keyboard/mouse while it’s running**  
- When done, you’ll see:

```
Expense filed! Please check by logging into GoExpense.
```

---

## Important Note for Mac Users

To allow automation to work correctly, you must grant permission to the app to control Chrome:

- Go to:  
  `System Settings > Privacy & Security > Automation`  
- Enable Chrome access for the terminal or IDE used to run Docker  

---

## Security Note

- This app runs fully locally — nothing is uploaded or shared externally (except to OpenAI for image parsing)  
- OpenAI access is handled via your API key  

---
