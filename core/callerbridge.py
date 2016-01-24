import requests

def call(old_post, number):
    print old_post
    print number
    r = requests.post("http://8877cd2d.ngrok.io/api/Twilio/Call", data = {"post_id": old_post["post_id"], "post": old_post["post"], "number": number})
    print r.content
    