from flask import Flask, render_template
from speech_analysis import *
import os
app = Flask(__name__)
os.getcwd()


@app.route('/')
def index():
    return render_template("index.html")


#background process happening without any refreshing
@app.route('/record')
def record():
    print("Hello")
    record_audio(30)
    return("nothing")

#background process happening without any refreshing
@app.route('/process')
def process():
    print("started processing")
    features = calculate_features("output.wav", "/Users/louis/Google Drive/adele-rutuja-louis/data")
    print("finished processing")
    return render_template("result.html", result = features)


if __name__ == "__main__":
    app.run(debug=True)