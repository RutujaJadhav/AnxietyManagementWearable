from flask import Flask, make_response, request, Blueprint, render_template, redirect, url_for, send_from_directory, flash
from speech_analysis import *
import pyrebase
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
import urllib.request

app = Flask(__name__)
# os.getcwd()

config = {
    "apiKey": "AIzaSyBR2lMqSAavdwi-JKr_5FQ64GDQFjtRjAY",
    "authDomain": "anxietywearable.firebaseapp.com",
    "databaseURL": "https://anxietywearable.firebaseio.com",
    "storageBucket": "anxietywearable.appspot.com",
}

cloudinary.config(
  cloud_name = "dsuutm3lg",
  api_key = "982542493312584",
  api_secret = "gMZK5dnAklio6UyMWkWjDFPGagA"
)

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Read data
db = firebase.database()

# Get previous speech features
prev_speech = db.child("speech_features").child("previous").get().val()

file_url = {"url":"blank"}

# Landing page
@app.route('/')
def index():
    return render_template("index.html")


# Record audio
@app.route('/record', methods = ['POST'])
def record():
    # f = open('./file.wav', 'wb')
    # f.write(request.data)
    print(type(request.data))
    response = cloudinary.uploader.upload(request.data,
              public_id = "file",
              overwrite = True,
              resource_type = "video")

    print(response['url'])
    file_url["url"] = response['url']
    print(file_url["url"])
    print("GOT HERE")
    return("Binary message written!")

# Process speech
@app.route('/process', methods=['POST'])
def process():
    print("URL IS THIS:",file_url)
    #Save speech file from url
    urllib.request.urlretrieve(file_url["url"], "file.wav")

    # get path of speech file
    path = os.path.realpath("./file.wav").split("/file.wav")[0] 

    # calculate features of speech
    features = calculate_features("file.wav", path) 

    # calculate difference between current and previous speech
    features_diff = calculate_difference(features, prev_speech) 

    db.child("speech_features").child("previous").set(features)

    return render_template("result.html", result = features_diff)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)