from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime, timedelta
import pymongo
import sys
sys.path.append('../')
import config
import consequences.facebook as facebook
import consequences.venmo as venmo
import callerbridge



### README:
### 1) Set up a Redis server (redis-server)
### 2) Provide the host, port, password, uncomment the Queue in the Redis instance below (connection=Redis(#host=, port=))
### 3) Run the rqscheduler script on the same machine as the Redis server
### 4) Call schedule(). Should work

# q = Queue("twilio-jobs")
scheduler = Scheduler(connection=Redis())


def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://" + config.MONGO_USER + config.MONGO_PASS + "@" + config.MONGO_HOST + "/" + config.MONGO_DB + "?authSource=admin")
    db = client['db']
    return db


def schedule(time, consequence, number):
    # something like this. The syntax is time, method, args
    # time should be a UTC datetime object, consequence is one of: 'facebook', number is a 10 digit int
    twilio_call = lambda x: 1
    if consequence is "facebook":
        old_post = facebook.main()
    if consequence is "venmo":
        old_post = None
    # something like this. The syntax is time, method, args, kwargs
    args = [old_post, number]
    keywords = {'old_post': old_post, 'number': number}
    scheduler.enqueue_at(time, callerbridge.call, None, keywords)  # Date time should be in UTC



def get_jobs(number):
    jobs = scheduler.get_jobs(with_times=True)
    matches = []
    for job in jobs:
        if job.kwargs.number == number:
            matches.append(job)
    return matches


def unschedule(job_id):
    if job_id in scheduler.get_jobs():
        scheduler.cancel(job_id)
    else:
        raise TypeError("No such job ID " + job_id + " found! ")
