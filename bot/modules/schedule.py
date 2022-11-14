from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Schedule:

    def __init__(self, tasks: list):
        self.scheduler = AsyncIOScheduler()
        self.time = 60 * 8
        self.add_tasks(tasks)

    def add_tasks(self, tasks: list):
        for task in tasks:
            self.scheduler.add_job(task, 'interval', minutes=self.time)

    def start(self):
        self.scheduler.start()
        logger.info('Schedule started')
