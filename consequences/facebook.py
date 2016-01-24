import requests
import sys
import config
from pymongo import MongoClient

sys.path.append('../')

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


# Get facebook access token
def get_access_token(phone):
    db = connect_to_mongo()
    access_token_dict = db.users.find_one({'phone_number': phone}, {'consequences.facebook.access_token': 1, '_id': 0})
    access_token = access_token_dict['consequences']['facebook']['access_token']
    print access_token

    return access_token


# Get last_date used
def get_last_date(phone):
    db = connect_to_mongo()
    last_date_dict = db.users.find_one({'phone_number': phone}, {'consequences.facebook.last_date': 1, '_id': 0})
    if 'last_date' in last_date_dict['consequences']['facebook']:
        last_date = last_date_dict['consequences']['facebook']['last_date']
    else:
        last_date = 0
    print 'Last date : ' + str(last_date)
    return last_date


# Update the last_date used for getting a user's post
def update_last_date(phone, date):
    return None


# Get earliest unused facebook post
def get_old_post(phone):
    # global access_token
    print "GETTING ACCESS TOKEN FROM DB"
    access_token = get_access_token(phone)
    print access_token
    print "GOT ACCESS TOKEN"
    last_date = get_last_date(phone)
    if last_date is None:
        print "No last date found, resetting to 0"
        last_date = 0

    fields = 'id,created_time,updated_time,message,likes'
    until = '1453587145'
    filter = 'app_2915120374'
    limit = '500'

    params = {'fields': fields,
              'until': until,
              'filter': filter,
              'limit': limit,
              'access_token': access_token}

    print "MAKING REQUEST"
    response_json = requests.get('https://graph.facebook.com/v2.5/me/posts', params=params).json()
    print response_json
    return response_json


# Share post
def share_post_using_id(post_id):
    pass


def main():
    get_access_token("9145632336")

if __name__ == '__main__':
    main()
