from flask import Flask , render_template , request
from urllib.parse import urlparse
from difflib import SequenceMatcher
app = Flask(__name__)
attempts = []
count = 0
@app.route("/")
def home():
    return render_template("login.html")
@app.route("/login",methods = ["POST"])
def login():
    global count
    username = request.form.get("name")
    password = request.form.get("password")
    count += 1
    attempts.append({

        "username_lenght" :count
        ,
        "time" : "Now"
    })

    return render_template("result.html",username = username , password = password , attempts = attempts)

@app.route("/url_chacker" , methods = ["GET","POST"])
def check():
    trusted_sites = [
    "google", "gmail", "facebook",
    "instagram", "twitter", "amazon",
    "paypal", "netflix", "microsoft"
    ]
    if request.method == "POST":
        url = request.form.get("url")
        result = "safe"
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        name = domain.split(".")[0]
        for site in trusted_sites:
            ratio = SequenceMatcher(None , site , name).ratio()
            if ratio > 0.8 and ratio < 1.0 or "http://" in url:
                result = "Suspicious"
                break
            elif ratio == 1.0:
                result = "safe"
                break
            else:
                result = "unknown"
        return render_template("url_chacker.html" , result = result)
    else:
        return render_template("url_chacker.html")



