import requests


def call(old_post, number):
    url = 'http://hotlinering.com/api/Twilio/Call'
    if old_post:
        r = requests.post(url, data = {"number": number, "cons": 'venmo'})
        print r.content
    else:
        r = requests.post(url, data = {"number": number, "post_id": old_post['post_id'], "post": old_post['post'], "cons": 'facebook'})
        print r.content
