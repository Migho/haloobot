import asyncio
import schedule
from haloobot.handlers.base import Handler
from haloobot.utils import time

class ScheduleHandler(Handler):

    SCHEDULE_TIME = "10:00"
    SLEEP_TIME = 10*60

    def __init__(self, handlers, bot, tables, messages, settings):
        super().__init__(handlers, bot, tables, messages, settings)
        schedule.every().day.at(self.SCHEDULE_TIME).do(self.send_to_all)
    
    async def schedule_loop(self):
        while True:
            schedule.run_pending()
            await asyncio.sleep(self.SLEEP_TIME)
    
    async def send_to_all(self):
        for result in self.tables['db'].query('SELECT DISTINCT chat_id FROM schedules'):
            await self.send_upcoming(result['chat_id'])
    
    async def send_upcoming(self, chat_id):
        ret = time.get_upcoming_events_string(self.tables['schedules'], chat_id)
        if ret:
            return await self.send_message(chat_id, '\n'.join(ret))
        else:
            return False



