from flask import Flask, render_template, session, redirect, request, flash
from flask_oauth import OAuth
import config
from consequences import facebook as fb_con
from core import core
from datetime import datetime

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
    request_token_params={'scope': 'email'}
)
'''
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='<your key here>',
    consumer_secret='<your secret here>'
)
'''


@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')


def create_datetime(hour_min_str):
    ptime = datetime.strptime(hour_min_str, "%H:%M")
    print ptime
    return ptime


@app.route("/")
def index():
    return render_template("index.html", session=session)


@app.route("/submit-call", methods=['POST'])
def submit_call():
    print request.form
    time = request.form['time']
    phone_number = request.form['phone']
    # connect and write token to mongo
    # later we can have a dict that gets updated based on what tokens are present
    db = fb_con.connect_to_mongo()
    update_status = db.users.update(
        {'phone_number': phone_number},
        {'$set': {'consequences.facebook.access_token': session['facebook_token']}},
        True
    )
    print update_status

    # schedule a call
    core.schedule(create_datetime(time), 'facebook', phone_number)

    return render_template("index.html", session=session)


@app.route("/login/facebook")
def login_facebook():
    # return facebook.authorize(callback=url_for('oauth_authorized',
    return facebook.authorize(callback="http://localhost:5000/facebook-oauth-authorized")
    # next=request.args.get('next') or request.referrer or None)


@app.route('/facebook-oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
    # next_url = request.args.get('next') or url_for('index')
    next_url = request.args.get('next') or 'http://localhost:5000/'
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['facebook_token'] = resp['access_token']
    session['facebook_token_expires'] = resp['expires']

    flash('You were signed in to Facebook with token %s' % resp['access_token'])
    return redirect(next_url)

if __name__ == "__main__":
    app.secret_key = app.config['APP_SECRET_KEY']
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
