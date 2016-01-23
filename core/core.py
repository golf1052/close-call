from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
import pymongo
import config

scheduler = Scheduler(connection=Redis())

def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://" + config.MONGO_USER + config.MONGO_PW + "@" + MONGO_IP)
    db = client[db]
    return db


def schedule(time, consequence, number):
    #something like this. The syntax is time, method, args
    scheduler.enqueue_at(strptime(time), twilio.call, number, consequence) # Date time should be in UTC


def unschedule(number):
    if user.job_id in scheduler.get_jobs():
        scheduler.cancel(user.job_id)
