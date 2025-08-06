---

# AutoExpense: Automated Expense Filing with GPT-4o + Selenium

AutoExpense is a local web application that automates the process of filing expenses on the GoExpense platform.

Using a Flask + React-style frontend, OpenAI’s GPT-4o for reading receipt images (including PDFs, PNGs, JPEGs), and Selenium to control Chrome, it simplifies expense submission into a drag-and-drop experience.

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

---

## How to Use

### Step 1: Pull the Docker Image

```bash
docker pull rkaushik302/expense_file_automate:v0
```

---

### Step 2: Run the Container

Replace `<HOST_PORT>` with any open local port (e.g. `5000`) and insert your OpenAI API key.

```bash
docker run -p <HOST_PORT>:5001 -e OPENAI_API_KEY="your-openai-api-key" rkaushik302/expense_file_automate:v0
```

---

### Step 3: Open the App in Your Browser

Go to:

```
http://127.0.0.1:<HOST_PORT>
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

To allow automation to work correctly, you must grant permission to the app running Docker to control Chrome:

- Go to:  
  `System Settings > Privacy & Security > Automation`  
- Enable Chrome access for the terminal or IDE used to run Docker  

---

## Security Note

- This app runs fully locally — nothing is uploaded or shared externally (except to OpenAI for image parsing)  
- OpenAI access is handled via your API key  

---
