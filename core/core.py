from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
from pymongo import mongo
import config

scheduler = Scheduler(connection=Redis())
client = pymongo.MongoClient("mongodb://" + config.MONGO_USER + config.MONGO_PW + "@" + MONGO_IP)
db = client.admin


def schedule(time, token, module, number):
    #something like this. the module doing the calling has to deal with results
    new_id = scheduler.enqueue_at(strptime(time), twilio.call, token, name) # Date time should be in UTC
    #this is still a dumb schema
    db.closecall.users.update(
      { "phone_number" : number },
      { $set: { "job" : new_id  }},
      )

def unschedule(key):
    #get jobid from mongo using key/token?
    if job_id in scheduler.get_jobs():
        scheduler.cancel(job_id)
