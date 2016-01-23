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
    access_token_dict = db.users.find_one({'phone_number': phone}, {'access_tokens.facebook': 1, '_id': 0})
    access_token = access_token_dict['access_tokens']['facebook']
    print access_token
    get_old_post()

# Get random old facebook post
def get_old_post():
    global access_token
    query = 'SELECT post_id, message, permalink, created_time ' \
        'FROM stream ' \
        'WHERE source_id = me() ' \
        'AND is_hidden != \"true\" ' \
        'AND type = 46 ' \
        'ORDER BY created_time ASC ' \
        'LIMIT 2'
    params = urllib.urlencode({'q':query, 'access_token':access_token})
    response = requests.get('https://graph.facebook.com/v2.0/fql?' + params)
    print response.json()

    return
def main():
    get_access_token("9145632336")

if __name__ == '__main__':
    main()
