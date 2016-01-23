from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
import pymongo
import config
import consequences.facebook as facebook

scheduler = Scheduler(connection=Redis())

def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://" + config.MONGO_USER + config.MONGO_PW + "@" + MONGO_IP)
    db = client[db]
    return db


def schedule(time, consequence, number):
    if consequence is "facebook":
        old_post = facebook.main()
    #something like this. The syntax is time, method, args
    scheduler.enqueue_at(strptime(time), twilio.call, number, old_post) # Date time should be in UTC


def unschedule(number):
    if user.job_id in scheduler.get_jobs():
        scheduler.cancel(user.job_id)
