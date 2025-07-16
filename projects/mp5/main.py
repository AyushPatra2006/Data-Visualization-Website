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

# Our data source: this loads the data we'll serve as HTML and JSON
df = pd.read_csv("main.csv")

app = Flask(__name__)

# ✅ GLOBAL VARIABLES FOR A/B TESTING
homepage_visits = 0
clicks_from_A = 0
clicks_from_B = 0
locked_version = None

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!