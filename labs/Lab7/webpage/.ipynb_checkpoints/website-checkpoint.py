from flask import Flask, request

my320app = Flask("example-server")
home_visits = 0
donate_visits = 0
def count_donate():
    global donate_visits
    donate_visits += 1
    print("VISITER", donate_visits)
def count_home():
    global home_visits
    home_visits += 1

@my320app.route("/")
def home():
    count_home()
    ctr = (donate_visits / home_visits) * 100 if home_visits > 0 else 0
    with open("index.html") as f:
        html = f.read()
    # the variable html is just a string, and can be changed with basic string methods
    html = html.replace("xyz", f"{ctr:.2f}% ({donate_visits} / {home_visits})")
    return html

@my320app.route("/donate.html")
def donate():
    count_donate()
    return """<html><body style="background-color:lightblue">
              <h1>Donations</h1>
              Please make one!
              <body></html>"""

if __name__ == '__main__':
    my320app.run("0.0.0.0", "5000", debug=True, threaded=False)