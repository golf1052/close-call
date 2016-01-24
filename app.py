from flask import Flask, render_template, session, redirect, request, flash, url_for
from flask_oauth import OAuth
from consequences import facebook as fb_con
from consequences import venmo as vmo
from core import core

import datetime
import time
import config
import requests

app = Flask(__name__)
app.config.from_object(config)

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_CONSUMER_KEY'],
    consumer_secret=app.config['FACEBOOK_CONSUMER_SECRET'],
    request_token_params={'scope': 'user_posts,publish_actions'}
)


@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')


def create_datetime(hour_min_str):
    # ptime = datetime.datetime.strptime(hour_min_str, "%H:%M")
    ptime = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(hour_min_str, "%H:%M").time())
    print ptime
    return ptime 

@app.route("/")
def index():
    return render_template("index.html", session=session)


def mongo_update(phone_number, key, value):
    db = fb_con.connect_to_mongo()

    update_status = db.users.update(
        {'phone_number': phone_number},
        {'$set': {key: value}},
        True
    )

    return update_status


@app.route("/submit-call", methods=['POST'])
def submit_call():
    print request.form
    time = request.form['time']
    phone_number = request.form['phone']
    # venmo_or_fb = request.form['venmo_or_fb']

    # connect and write token to mongo
    if session['facebook_token']:
        fb_status = mongo_update(phone_number, 'consequences.facebook.access_token', session['facebook_token'])
        core.schedule(create_datetime(time), 'facebook', phone_number)
        print fb_status

    if session['venmo_token']:
        venmo_status = mongo_update(phone_number, 'consequences.venmo.access_token', session['venmo_token'])
        core.schedule(create_datetime(time), 'venmo', phone_number)
        print venmo_status

    return render_template("index.html", session=session)


@app.route("/login/facebook")
def login_facebook():
    return facebook.authorize(callback="http://localhost:5000/facebook-oauth-authorized")


@app.route("/login/venmo")
def login_venmo():
    return redirect('https://api.venmo.com/v1/oauth/authorize?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}'.format(
        client_id=app.config['VENMO_CLIENT_ID'],
        scope='make_payments,access_friends,access_payment_history,access_feed',
        redirect_uri='http://localhost:5000/venmo-oauth-authorized'
        ))


def extend_facebook_token(existing_token):
    params = {
            'client_id': app.config['FACEBOOK_APP_ID'],
            'client_secret': app.config['FACEBOOK_APP_SECRET'],
            'redirect_uri': 'http://localhost:5000/',
            'access_token': existing_token,
            }
    response = requests.get('https://graph.facebook.com/oauth/client_code', params=params)
    code = response.json()['code']

    params = {
            'client_id': app.config['FACEBOOK_APP_ID'],
            'redirect_uri': 'http://localhost:5000/',
            'code': code,
            }
    response = requests.get('https://graph.facebook.com/oauth/access_token', params=params)
    resp = response.json()
    # if there are weird time issues, utcnow could be to blame
    return (resp['access_token'],
            time.mktime((datetime.datetime.utcnow() + datetime.timedelta(seconds=resp['expires_in'])).timetuple()))


@app.route('/facebook-oauth-authorized')
@facebook.authorized_handler
def facebook_oauth_authorized(resp):
    next_url = request.args.get('next') or 'http://localhost:5000/'
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['facebook_token'] = resp['access_token']
    session['facebook_token_expires'] = resp['expires']

    # exchange short lived token for long lived
    long_token, expires = extend_facebook_token(resp['access_token'])
    session['facebook_token'] = long_token
    session['facebook_token_expires'] = expires

    flash('You were signed in to Facebook with token %s' % resp['access_token'])
    return redirect(next_url)


@app.route('/venmo-oauth-authorized')
def venmo_oauth_authorized():
    auth_code = request.args.get('code')

    data = {
            'client_id': app.config['VENMO_CLIENT_ID'],
            'client_secret': app.config['VENMO_CLIENT_SECRET'],
            'code': auth_code,
            }

    response = requests.post('https://api.venmo.com/v1/oauth/access_token', data)
    resp = response.json()

    session['venmo_token'] = resp['access_token']
    session['venmo_user'] = resp['user']['username']
    session['venmo_refresh_token'] = resp['refresh_token']
    session['venmo_token_expires'] = resp['expires_in']

    flash('You were signed in to venmo with username %s token %s' % (resp['user']['username'], resp['access_token']))
    return redirect(url_for('index'))
    
# Bridge code
@app.route('/bridge/facebook', methods=['POST'])
def bridge_facebook():
    fb_con.share_post_using_id(request.form.get('number'), request.form.get('post_id'))
    
@app.route('/bridge/venmo', methods=['POST'])
def bridge_venmo():
    vmo.make_payment(request.args.get('number'))

if __name__ == "__main__":
    app.secret_key = app.config['APP_SECRET_KEY']
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
