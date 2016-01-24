import requests
import indicoio
import itertools
import operator
import config
import random
from pymongo import MongoClient
from collections import namedtuple

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
    return access_token


Post = namedtuple('Post', ['id', 'date', 'message', 'likes', 'score'])

# Score post based on a bunch of heuristics determined by world renown research methods (aka trial and error)
def score_post(likes, sentiment, tags, personalities):
    base_score = 1

    sentiment_score = 1 / sentiment

    likes_score = 0.1 * likes

    bonus_tags = {
            'anime': 3,
            'art': 1,
            'atheism': 4,
            'business': 1,
            'conspiracy': 5,
            'drugs': 5,
            'music': 1,
            'personal': 4,
            'psychology': 1,
            'relationships': 10,
            'romance': 5,
            'ultimate': 1,
            'writing': 1,
            'poetry': 3,
            'gender_issues': 10,
            'personal_care_and_beauty': 5,
            'school': 5,
            }

    bonus_tag_score = 5
    tag_threshold = 0.02

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

        posts.append(Post(post['id'], post['created_time'],post['message'], likes, None))
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

        # Sentiment analysis debugging
        # top_tags = sorted(tags.items(), key=operator.itemgetter(1), reverse=True)
        # top_tags = top_tags[:10]
        # print '\n=========================================================='
        # print post.message
        # for key, val in top_tags: print "%s: %0.5f" % (key, val)

        posts_list.append(Post(post.id, post.date, post.message, post.likes, score_post(likes, sentiment, tags, personalities)))
    posts_list.sort(key=get_score, reverse=True)
    return random.choice(posts_list[:len(posts_list)/2])

def get_score(post):
    return post.score

# Get earliest unused facebook post
def get_old_post(phone):
    # global access_token
    print "GETTING ACCESS TOKEN FROM DB"
    access_token = get_access_token(phone)
    print access_token
    print "GOT ACCESS TOKEN"

    fields = 'id,created_time,message,likes'
    until = '1264342952'
    type_filter = 'app_2915120374'
    limit = '500'

    params = {'fields': fields,
              'until': until,
              'filter': type_filter,
              'limit': limit,
              'access_token': access_token}

    print "MAKING REQUEST"
    response_json = requests.get('https://graph.facebook.com/v2.5/me/posts', params=params).json()
    if 'data' in response_json:
        print "GOT A LIST OF POSTS BACK"
    elif 'error' in response_json:
        return {'error': response_json['error']['type'],
                'message': response_json['error']['message']}

    top_cringe = choose_post(response_json)
    year = top_cringe.date[:4]
    return_dict = {'post_id': top_cringe.id,
                   'post': 'Here is something you posted in ' + year + '|' + top_cringe.message}

    print "post_id: %s\npost: %s" % (return_dict['post_id'], return_dict['post'])
    return return_dict


# Because facebook are fuckers
def get_post_url(post_id):
    post_id_arr = post_id.split('_')
    if len(post_id_arr) == 2:
        return 'https://www.facebook.com/' + post_id_arr[0] + '/posts/' + post_id_arr[1]
    else:
        raise Exception('This is not a valid post_id: ' + post_id)

# Share post on facebook
def share_post_using_id(phone, post_id):
    post_url = get_post_url(post_id)
    access_token = get_access_token(phone)

    params = {'link': post_url,
              'message': 'Public shaming brought to you by http://hotlinering.com',
              'access_token': access_token}
    print "POSTING TO FACEBOOK"
    response_json = requests.post('https://graph.facebook.com/v2.5/me/feed', params=params).json()
    if 'error' in response_json:
        return {'error': response_json['error']['type'],
                'message': response_json['error']['message']}
    else:
        print 'SUCCESS! New Post URL is ' + get_post_url(response_json['id'])

def main():
    #For Testing
    #share_post_using_id("6172300310", '10208690008351449_215666932687')
    get_old_post('9145632336')

if __name__ == '__main__':
    main()
