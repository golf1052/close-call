import requests
import sys
sys.path.append('../')
import config
from pymongo import MongoClient
import random

access_token = ''


# Connects to mongo and returns a MongoClient
def connect_to_mongo():
    host = config.MONGO_HOST
    user = config.MONGO_USER
    password = config.MONGO_PASS
    db = config.MONGO_DB
    connection_url = "mongodb://" + user + ":" + password + "@" + host + "/" + db + "?authSource=admin"
    client = MongoClient(connection_url)

    return client[db]


# get "me" (whoever the access token is registered to)
def get_profile(phone):
    access_token = get_access_token(phone)
    params = {'access_token': access_token}
    response_json = requests.get('https://api.venmo.com/v1/me', params=params).json()
    print response_json


# get all payments for the token's user
def get_payments(phone):
    access_token = get_access_token(phone)
    params = {'access_token': access_token}
    response_json = requests.get('https://api.venmo.com/v1/payments', params=params).json()
    print response_json


def make_payment(phone):
    access_token = get_access_token(phone)
    who_to_pay = random.choice(config.VENMO_USER_IDS) # randomly selected recepient of donor money
    params = {'access_token': access_token,
              'user_id': who_to_pay,
              'note': 'Public shaming brought to you by http://hotlinering.com',
              'amount': "1.00",
              'audience': "public"}
    response_json = requests.post('https://api.venmo.com/v1/payments', params=params).json()
    print response_json


# Get venmo access token
def get_access_token(phone):
    db = connect_to_mongo()
    access_token_dict = db.users.find_one({'phone_number': phone}, {'consequences.venmo.access_token': 1, '_id': 0})
    access_token = access_token_dict['consequences']['venmo']['access_token']
    print access_token
    return access_token
