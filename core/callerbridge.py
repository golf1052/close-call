import requests

def call(old_post, number):
    print old_post
    print number
    r = requests.post("http://1af2b38b.ngrok.io/api/Twilio/Call", data = {"post": old_post, "number": number})
    print r.content
    