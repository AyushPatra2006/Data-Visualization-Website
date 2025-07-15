'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP5
Student 1: Ayush Patra, apatra8
Student 2: <Name>, <NETID>
Student 3: <Name>, <NETID>
Student 4: <Name>, <NETID>
'''
import pandas as pd
from flask import Flask, request, jsonify

# TODO: Add a comment about your data source

app = Flask(__name__)
df = pd.read_csv("main.csv")

@app.route('/')
def home():
    with open("index.html") as f:
        html = f.read()

    return html

@app.route('/browse.html')
def browse():
    with open("browse.html") as f:
        html = f.read()

    return html
@app.route('/donate.html')
def donate():
    with open("donate.html") as f:
        html = f.read()

    return html

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
