import requests
import urllib
import sys
from pymongo import MongoClient
sys.path.append('../')
import config

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
    global access_token
    access_token_dict = db.users.find_one({'phone_number': phone}, {'consequences.facebook.access_token': 1, '_id': 0})
    access_token = access_token_dict['consequences']['facebook']['access_token']
    print access_token
    get_old_post(phone)

# Get last_date used
def get_last_date(phone):
    db = connect_to_mongo()
    last_date_dict = db.users.find_one({'phone_number': phone}, {'consequences.facebook.last_date': 1, '_id': 0})
    last_date = last_date_dict['consequences']['facebook']['last_date']
    print 'Last date : ' + str(last_date)
    return last_date

# Update the last_date used for getting a user's post
def update_last_date(phone, date):
    return date

# Get earliest unused facebook post
def get_old_post(phone):
    global access_token
    last_date = get_last_date(phone)
    if last_date is None:
        print "No last date found, resetting to 0"
        last_date = 0
    query = 'SELECT post_id, message, permalink, created_time ' \
        'FROM stream ' \
        'WHERE source_id = me() ' \
        'AND is_hidden != \"true\" ' \
        'AND type = 46 ' \
        'AND created_time > ' + str(last_date) + ' ' \
        'ORDER BY created_time ASC ' \
        'LIMIT 5'
    params = urllib.urlencode({'q': query, 'access_token': access_token})
    response_json = requests.get('https://graph.facebook.com/v2.0/fql?' + params).json()
    post_dict = {'post_id': response_json['data'][0]['post_id'], 'post': response_json['data'][0]['message']}
    print post_dict

# Share post
def share_post_using_id(post_id):
    
def main():
    get_access_token("9145632336")

if __name__ == '__main__':
    main()
