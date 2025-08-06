from flask import Flask, render_template, request, jsonify
import time
from automator import file_expense
import re

app = Flask(__name__)

# extract data from the request form
def parse_expenses_from_request(request):
    expense_rows = []

    # Step 1: Figure out how many rows we have
    row_ids = set()

    for key in request.form.keys():
        match = re.match(r"(case_code|reason|type)_(\d+)", key)
        if match:
            row_ids.add(match.group(2))

    for row_id in sorted(row_ids, key=int):
        row = {
            "case_code": request.form.get(f"case_code_{row_id}", "").strip(),
            "type": request.form.get(f"type_{row_id}", "").strip(),
            "reason": request.form.get(f"reason_{row_id}", "").strip(),
            "files": request.files.getlist(f"file_{row_id}")  # may be empty []
        }
        expense_rows.append(row)

    return expense_rows

# Show index page
@app.route("/")
def index():
    return render_template("index.html")

# Caching user credentials
@app.route("/credentials", methods=["GET"])
def check_cached_credentials():
    if cached_credentials:
        return jsonify({"has_credentials": True})
    else:
        return jsonify({"has_credentials": False})

# Submit expenses
cached_credentials = {}
@app.route("/submit", methods=["POST"])
def submit():
    global cached_credentials
    data = request.form
    username = data.get("username")
    password = data.get("password")

    if username and password:
        cached_credentials = {"username": username, "password": password}
    elif cached_credentials:
        username = cached_credentials["username"]
        password = cached_credentials["password"]
    else:
        return jsonify({"error": "Credentials required"}), 400

    expenses = parse_expenses_from_request(request)

    script = f'''
    delay 1
    tell application "System Events"
        keystroke "{username}"
        keystroke tab
        keystroke "{password}"
        keystroke return
    end tell
    '''

    with open("login.scpt", "w") as f:
        f.write(script)

    # Here’s where you call your automation logic
    # You can pass parsed data and files to it
    print("Running automation with for ", username)
    tic = time.time()
    file_expense(expenses)
    toc = time.time()
    print(f"Automation for {username} ran for {(toc - tic)//60}min{(round(toc - tic))%60}sec!")

    time.sleep(3)  # simulate work
    return jsonify({"status": "success", "message": "Expense filed! Please check by logging into GoExpense"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)