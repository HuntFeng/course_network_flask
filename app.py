from flask import Flask, request, render_template
from visualization import make_graph
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    raw_string = None
    if request.method == "POST":
        raw_string = request.form["subjects"]
    raw_string = "math, bus" if raw_string == None else raw_string
    graph(raw_string)
    return render_template("index.html", subject_list=raw_string)

def graph(raw_string):
    # raw_string has the following format
    # Mathematics, phys, Macm, CMPT
    # need to make them all lower case and put them into a list
    subjects = pd.read_json("subject_list.json")
    subject_label = subjects["label"]
    subject_name = subjects["name"].apply(lambda x: x.lower())

    subject_list = [] # subjects to be drawn
    string_list = raw_string.split(",")
    for n, string in enumerate(string_list):
        s = string.strip().lower()
        if subject_label.isin([s]).any():
            subject_list.append(s)
        elif subject_name.isin([s]).any():
            subject = subjects[subject_name.isin([s])]["label"].item()
            subject_list.append(subject)
    
    make_graph(subject_list)

if __name__ == "__main__":
    app.run(debug=True)