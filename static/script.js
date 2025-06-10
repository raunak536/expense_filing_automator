let rowCount = 0;
const expenseTypes = [
  "Meals - Late/OT @ Home",
  "Meals - Business Travel"
];

function addRow() {
  rowCount++;
  const row = document.createElement("div");
  row.className = "expense-row";

  let typeSelect = `<select name="type_${rowCount}">`;
  expenseTypes.forEach(type => {
    typeSelect += `<option value="${type}">${type}</option>`;
  });
  typeSelect += `</select>`;

  row.innerHTML = `
    <span>${rowCount}</span>
    <input name="case_code_${rowCount}" placeholder="Case Code">
    <input name="reason_${rowCount}" placeholder="Reason">
    ${typeSelect}
    <input type="file" name="file_${rowCount}" multiple>
  `;

  document.getElementById("expense-rows").appendChild(row);
}

//function addRow() {
//    rowCount++;
//    const row = document.createElement("div");
//    row.className = "expense-row";
//    row.innerHTML = `
//        <span>${rowCount}</span>
//        <input name="case_code_${rowCount}" placeholder="Case Code">
//        <input name="type_${rowCount}" placeholder="Type">
//        <input name="reason_${rowCount}" placeholder="Reason">
//        <input type="file" name="file_${rowCount}" multiple>
//    `;
//    document.getElementById("expense-rows").appendChild(row);
//}

// show modal
//function showLogin() {
//    document.getElementById("login-modal").style.display = "block";
//}

function showLogin() {
  fetch("/credentials")
    .then(res => res.json())
    .then(data => {
      if (data.has_credentials) {
        // ✅ Credentials already cached — just submit the form
        submitForm();
      } else {
        // ❌ No cached credentials — show modal
        document.getElementById("login-modal").style.display = "block";
      }
    });
}
// on modal submit
function submitForm() {
    const formData = new FormData(document.getElementById("expense-form"));
    formData.append("username", document.getElementById("username").value);
    formData.append("password", document.getElementById("password").value);

    document.getElementById("login-modal").style.display = "none";
    document.getElementById("progress").classList.remove("hidden");

    const bar = document.getElementById("bar");
    bar.value = 0;
    const interval = setInterval(() => {
        bar.value += 10;
        if (bar.value >= 100) clearInterval(interval);
    }, 300);

    fetch("/submit", {
        method: "POST",
        body: formData
    }).then(res => res.json()).then(data => {
        alert(data.message);
        document.getElementById("progress").classList.add("hidden");
    });
}