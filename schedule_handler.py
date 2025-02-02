import os
import threading
from typing import Callable, Dict
import pandas as pd
import schedule

from commonkit.logging.logging_config import LogConfig
from commonkit.utilities.datetime_utilities import DatetimeUtilities
import csv



log_config = LogConfig(__name__)
logger = log_config.logger
class SchedulerHandler:
    plan: Dict[int, pd.DataFrame]
    chat_id_schedule: Dict[int, str]
    db_file_path: str
    callback_func: Callable[[str, str], None]
    def __init__(self, callback_func: Callable[[str, str], None]):
        folder_path = './files/database/'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        self.db_file_path = os.path.join(folder_path, "database.csv")
            
        self.chat_id_schedule = {}
        self.plan = {}
        self.callback_func = callback_func
    
    def weekday_pairer(self, key: int):
        weekday = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        return weekday[key]
    def start_all_schedules(self):
        all_schdule_df = pd.DataFrame(pd.read_csv(self.db_file_path))
        for row in all_schdule_df.iterrows():
            chat_id = row[1]['chat_id']
            file_name = row[1]['file_name']
            self.create_user_schedule(chat_id=chat_id, file_name=file_name)

    def create_user_schedule(self, chat_id: str, file_name: str):
        self.chat_id_schedule[chat_id] = file_name
        self.plan[chat_id] = pd.DataFrame(pd.read_excel(self.chat_id_schedule[chat_id]))
        
        thread = threading.Thread(
            target=self.scheduler, args=[chat_id, self.callback_func,])
        thread.daemon = True
        thread.start()

    def save_chat_id_schedule_to_csv(self, sender, chat_id, file_name: str):
            
            with open(self.db_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['sender', 'chat_id', 'file_name'])
                
                writer.writerow([sender, chat_id, file_name])

    def get_task(self, task_index, chat_id):
        now = DatetimeUtilities.now()
        weekday = now.weekday()
        weekday_str = self.weekday_pairer(weekday)
        task = self.plan[chat_id][weekday_str][task_index]
        return task
    
    def scheduler(self, chat_id):
        columns = self.plan[chat_id].columns
        timeline = self.plan[chat_id][columns[0]]
        for i in range(len(timeline)):
            task = self.get_task(i, chat_id)
            time_str: str = timeline[i]
            start_time = time_str.split('-')[0]
            start_time_dt = DatetimeUtilities.str_to_datetime(dt_str=start_time, iso= False, fmt='%H:%M')
            def do():
                logger.info(start_time_dt.time().strftime('%H:%M')) 
                schedule.every().day.at(start_time_dt.time().strftime('%H:%M')).do(self.callback_func, chat_id, task)
                schedule.run_pending()
            th = threading.Thread(target=do)
            th.daemon = True
            th.start()
        while True:
            schedule.run_pending()
            
        