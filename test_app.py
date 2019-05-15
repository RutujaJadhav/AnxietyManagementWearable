from flask import Flask, render_template, Response, request, redirect, url_for
import os
from speech_analysis import *
from my_audio_analysis import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

#background process happening without any refreshing
@app.route('/record')
def background_process_test():
    print("Hello")
    return("nothing")


if __name__ == "__main__":
    app.run(debug=True)