from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler


# todo remove AsyncIOScheduler
class Schedule:

    def __init__(self, tasks: list):
        self.scheduler = AsyncIOScheduler()
        self.add_tasks(tasks)

    def add_tasks(self, tasks: list):
        for task in tasks:
            self.scheduler.add_job(task, 'interval', minutes=120)

    def start(self):
        self.scheduler.start()
        logger.info('Schedule started')
