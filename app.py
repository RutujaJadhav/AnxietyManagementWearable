from flask import Flask, make_response, request, Blueprint, render_template, redirect, url_for, send_from_directory, flash
from speech_analysis import *
import pyrebase
import os
app = Flask(__name__)
# os.getcwd()

config = {
    "apiKey": "AIzaSyBR2lMqSAavdwi-JKr_5FQ64GDQFjtRjAY",
    "authDomain": "anxietywearable.firebaseapp.com",
    "databaseURL": "https://anxietywearable.firebaseio.com",
    "storageBucket": "anxietywearable.appspot.com",
}

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Read data
db = firebase.database()

# Get previous speech features
prev_speech = db.child("speech_features").child("previous").get().val()

# Landing page
@app.route('/')
def index():
    return render_template("index.html")


# Record audio
@app.route('/record', methods = ['POST'])
def record():
    f = open('./file.wav', 'wb')
    f.write(request.data)
    print("GOT HERE")
    return("Binary message written!")

# Process speech
@app.route('/process')
def process():

    # get path of speech file
    path = os.path.realpath("./file.wav").split("/file.wav")[0] 

    # calculate features of speech
    features = calculate_features("file.wav", path) 

    # calculate difference between current and previous speech
    features_diff = calculate_difference(features, prev_speech) 

    db.child("speech_features").child("previous").set(features)

    return render_template("result.html", result = features_diff)


if __name__ == "__main__":
    app.run(debug=True)