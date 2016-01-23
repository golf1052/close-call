from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
from pymongo import mongo

scheduler = Scheduler(connection=Redis())
client = pymongo.MongoClient("mongodb://admin:yhackslackpack@104.131.125.189:27017")
db = client.admin


def schedule(time, token, module, name):
    #something like this. the module doing the calling has to deal with results
    new_id = scheduler.enqueue_at(strptime(time), twilio.call, token, name) # Date time should be in UTC
    #this is a dumb schema
    db.users.insert(
        {
        user_id: name,
        job_details: {
            token_type: module,
            secret_token: token,
            call_time: time,
            job_id: new_id
            }
        }
    )

def unschedule(key):
    #get jobid from mongo using key/token?
    if job_id in scheduler.get_jobs():
        scheduler.cancel(job_id)
