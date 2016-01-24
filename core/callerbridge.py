import requests

def call(old_post, number):
    r = requests.post("http://localhost:5999/api/Twilio/Call", data = {"post": old_post, "number": number});