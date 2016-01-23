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
    #something like this. The syntax is time, method, args, kwargs
    scheduler.enqueue_at(time, twilio.call, None, 'old_post'=old_post, 'number'=number)  # Date time should be in UTC

def get_jobs(number):
    jobs = scheduler.get_jobs(with_times=True)
    matches = []
    for job in jobs:
      if job.kwargs.number = number:
          matches.append(job)
    return matches

def unschedule(number):
    if job_id in scheduler.get_jobs():
        scheduler.cancel(user.job_id)
    else raise TypeError("No such job ID " + job_id + " found! ")
