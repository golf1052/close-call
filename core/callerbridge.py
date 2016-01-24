import requests

def call(old_post, number):
    url = 'http://localhost:5999/api/Twilio/Call'
    if old_post == None:
        r = requests.post(url, data = {"number": number, "cons": 'venmo'})
    else:
        r = requests.post(url, data = {"number": number, "post_id": old_post['post_id'], "post": old_post['post'], "cons": 'facebook'})
    