import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from angusbot import AngusBot

logging.basicConfig()
sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='6-8')
def scheduled_job():
    print("scheduled job running...")
    bot = AngusBot()
    bot.tweet()
    bot.favorite_mentions()
    print("...scheduled job completed")

sched.start()