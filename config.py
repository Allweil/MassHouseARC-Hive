import os

class Config:
    #flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "something_something"
    #google streetview api
    SIGNSECRET = "PxBaedk30oXYbqM4SP8vsfjNsmg"
    google_api_key = "AIzaSyB5yhms25XWbjWfdS3V5W4hTN2IdHlG0dc"
    #database
    host = 'localhost'
    user = 'kartikeya'
    password = 'cricketlover'
    database = "FB"
    charset='utf8mb4'



