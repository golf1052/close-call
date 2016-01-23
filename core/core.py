from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime

scheduler = Scheduler(connection=Redis())

def schedule(time, token, name):
    #something like this
    scheduler.enqueue_at(strptime(time), twilio.call, token, name) # Date time should be in UTC
