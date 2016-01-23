from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
import pymongo
import config

scheduler = Scheduler(connection=Redis())
client = pymongo.MongoClient("mongodb://" + config.MONGO_USER + config.MONGO_PW + "@" + MONGO_IP)
db = client.admin


def schedule(time, token, module, number):
    #something like this. the module doing the calling has to deal with results
    new_id = scheduler.enqueue_at(strptime(time), twilio.call, token, name) # Date time should be in UTC
    #this is still a dumb schema
    db.closecall.users.update(
        {"phone_number": number},
        {"$set": {"job_id": new_id}},
    )

def unschedule(number):
    user = db.closecall.users.find({"phone_number": number})
    if user.job_id in scheduler.get_jobs():
        scheduler.cancel(user.job_id)
