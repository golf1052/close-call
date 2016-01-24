import requests
import sys
import indicoio
import itertools
from pymongo import MongoClient
from collections import namedtuple
sys.path.append('../')
import config

access_token = ''

indicoio.config.api_key = config.INDICO_API_KEY


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


Post = namedtuple('Post', ['id', 'message', 'likes', 'score'])


def score_post(likes, sentiment, tags, personalities):
    base_score = 1

    sentiment_score = 1 / sentiment

    likes_score = 0.1 * likes

    bonus_tags = {
            'anime': 1,
            'art': 1,
            'atheism': 1,
            'business': 1,
            'conspiracy': 1,
            'drugs': 1,
            'music': 1,
            'personal': 1,
            'psychology': 1,
            'relationships': 1,
            'romance': 1,
            'ultimate': 1,
            'writing': 1,
            }

    bonus_tag_score = 0
    tag_threshold = 0.2

    for tag, multiplier in bonus_tags.iteritems():
        tag_score = tags[tag]

        if tag_score >= tag_threshold:
            bonus_tag_score += tag_score * float(multiplier)

    # low agreeableness, low conscientiousness, high extraversion
    agreeableness = 1 / personalities['agreeableness']
    conscientiousness = 1 / personalities['agreeableness']
    extraversion = 1 * personalities['extraversion']

    final_score = (base_score + sentiment_score + likes_score +
                   bonus_tag_score + agreeableness + conscientiousness + extraversion)

    return final_score


def choose_post(response_json):
    posts = []
    posts_messages = []
    data = response_json['data']
    for post in data:
        if 'message' not in post:
            continue

        likes = 0

        if 'likes' in post:
            likes = len(post['likes'])

        posts.append(Post(post['id'], post['message'], likes, None))
        posts_messages.append(post['message'])

    apis = ['sentiment_hq', 'text_tags', 'personality']

    analyses = indicoio.analyze_text(posts_messages, apis=apis)

    posts_list = []
    #for analysis_type, vals in analyses.iteritems():
    for post, text_tags, sentiment_hq, personality in itertools.izip(posts, *analyses.values()):
        likes = post.likes
        sentiment = sentiment_hq
        tags = text_tags
        personalities = personality

        posts_list.append(Post(post.id, post.message, post.likes, score_post(likes, sentiment, tags, personalities)))
    posts_list.sort(key=get_score, reverse=True)
    print posts_list[:5]
    return posts_list[0]

def get_score(post):
    return post.score

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

    fields = 'id,created_time,message,likes'
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
    if 'data' in response_json:
        print "GOT A LIST OF POSTS BACK"
    top_cringe = choose_post(response_json)
    return_dict = {'post_id': top_cringe.id,
                   'post': top_cringe.message}
    print return_dict
    return return_dict


# Because facebook are fuckers
def get_post_url(post_id):
    post_id_arr = post_id.split('_')
    if len(post_id_arr) == 2:
        return 'https://www.facebook.com/' + post_id_arr[0] + '/posts/' + post_id_arr[1]
    else:
        raise Exception('This is not a valid post_id: ' + post_id)

# Share post
def share_post_using_id(phone, post_id):
    post_url = get_post_url(post_id)
    access_token = get_access_token(phone)

    params = {'link': post_url,
              'message': 'Public shaming brought to you by http://hotlinering.com',
              'access_token': access_token}
    print "POSTING TO FACEBOOK"
    response_json = requests.post('https://graph.facebook.com/v2.5/me/feed', params=params).json()
    # ERROR CHECKING
    print response_json


def main():
    #share_post_using_id("9145632336", '10203497848945781_10204739673510619')
    get_old_post('9145632336')

if __name__ == '__main__':
    main()