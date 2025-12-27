'''
Project: MP5
Student 1: Ayush Patra, apatra8
Student 2: None
Student 3: None
Student 4: None
'''

import pandas as pd
from flask import Flask, request, jsonify, make_response
import time
import re
# Our data source: this loads the data we'll serve as HTML and JSON
df = pd.read_csv("main.csv")
import matplotlib
matplotlib.use('Agg')  # ✅ Required for backend
import matplotlib.pyplot as plt
import io
from flask import send_file

app = Flask(__name__)

# ✅ GLOBAL VARIABLES FOR A/B TESTING
homepage_visits = 0
clicks_from_A = 0
clicks_from_B = 0
locked_version = None
num_subscribed = 0
# ✅ GLOBAL FOR RATE LIMITING
last_request_time = {}

@app.route('/')
def home():
    global homepage_visits, locked_version

    homepage_visits += 1

    # Decide which version to serve
    if locked_version:
        version = locked_version
    elif homepage_visits <= 10:
        version = "A" if homepage_visits % 2 == 0 else "B"
    else:
        version = "A" if clicks_from_A >= clicks_from_B else "B"
        locked_version = version  # lock in after 10 visits

    # Load base HTML
    with open("index.html") as f:
        html = f.read()

    # Replace the donation link based on version
    if version == "A":
        html = html.replace("{{donate_link}}", '<a href="donate.html?from=A" style="color:blue;">Donate</a>')
    else:
        html = html.replace("{{donate_link}}", '<a href="donate.html?from=B" style="color:red;">Donate</a>')

    return html

@app.route('/browse.html')
def browse():
    with open("browse.html") as f:
        html = f.read()
    return html

@app.route('/donate.html')
def donate():
    global clicks_from_A, clicks_from_B

    from_version = request.args.get("from")
    if from_version == "A":
        clicks_from_A += 1
    elif from_version == "B":
        clicks_from_B += 1

    # Load normal donate page
    with open("donate.html") as f:
        html = f.read()
    return html

@app.route('/browse.json')
def browse_json():
    ip = request.remote_addr
    now = time.time()

    # Rate limit: max once per 60 seconds
    if ip in last_request_time:
        elapsed = now - last_request_time[ip]
        if elapsed < 60:
            retry_after = int(60 - elapsed)
            response = make_response(
                jsonify({"error": "Too Many Requests. Please wait before trying again."}), 429)
            response.headers["Retry-After"] = retry_after
            return response

    last_request_time[ip] = now

    # Load data fresh each time
    df = pd.read_csv("main.csv")
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route('/visitors.json')
def visitors_json():
    visitor_ips = list(last_request_time.keys())
    return jsonify(visitor_ips)
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if re.fullmatch(r"[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-z]{3}", email):# 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        with open("emails.txt") as f:
            num_subscribed = len([line for line in f if line.strip()])
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify("not a valid email")
@app.route('/dashboard1.svg')
def dashboard1():
    df = pd.read_csv("main.csv")
    bins = int(request.args.get("bins", 10))  # query param

    fig, ax = plt.subplots()
    ax.hist(df["rating"], bins=bins, color='skyblue', edgecolor='black')
    ax.set_title(f"Ratings Histogram ({bins} bins)")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")

    # Save to SVG
    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    plt.close(fig)
    buf.seek(0)

    # Optional: save locally
    with open("dashboard1.svg" if bins == 10 else "dashboard1-query.svg", "wb") as f:
        f.write(buf.getvalue())

    response = make_response(send_file(buf, mimetype="image/svg+xml"))
    response.headers["Content-Type"] = "image/svg+xml"
    return response

@app.route('/dashboard2.svg')
def dashboard2():
    df = pd.read_csv("main.csv")

    fig, ax = plt.subplots()
    df.boxplot(column="rating", by="genre", ax=ax, grid=False)
    ax.set_title("Rating by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Rating")
    plt.suptitle("")  # remove automatic suptitle from boxplot

    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    plt.close(fig)
    buf.seek(0)

    with open("dashboard2.svg", "wb") as f:
        f.write(buf.getvalue())

    response = make_response(send_file(buf, mimetype="image/svg+xml"))
    response.headers["Content-Type"] = "image/svg+xml"
    return response
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!
