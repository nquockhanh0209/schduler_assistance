import datetime
import os
import threading
from typing import Callable, Dict
import pandas as pd
import schedule

from commonkit.logging.logging_config import LogConfig
from commonkit.utilities.datetime_utilities import DatetimeUtilities
import csv

from enums.day_session import DaySession
from model.daily_plan import DailyPlan
from mongo.pymongo_base import PyMongo



log_config = LogConfig(__name__)
logger = log_config.logger
class SchedulerHandler:
    plan: Dict[int, pd.DataFrame]
    chat_id_schedule: Dict[int, str]
    chat_id_daily_schedule: Dict[int, DailyPlan]
    db_file_path: str
    callback_func: Callable[[str, str], None]
    mongo_db: PyMongo
    def __init__(self, callback_func: Callable[[str, str], None]):
        folder_path = './files/database/'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        self.db_file_path = os.path.join(folder_path, "database.csv")
        self.chat_id_daily_schedule = {}    
        self.chat_id_schedule = {}
        self.plan = {}
        self.callback_func = callback_func
        self.start_all_schedules()
        self.mongo_db = PyMongo(db_host='mongodb://admin:password@localhost:27017/', db_name='scheduler')
    
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
            target=self.scheduler, args=[chat_id])
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
    def set_daily_task(self, chat_id: int, task: str):
        if chat_id not in self.chat_id_daily_schedule:
            self.chat_id_daily_schedule[chat_id] = DailyPlan()
        self.chat_id_daily_schedule[chat_id].task = task
    def set_goal(self, chat_id: int, goal: str):
        if chat_id not in self.chat_id_daily_schedule:
            self.chat_id_daily_schedule[chat_id] = DailyPlan()
        self.chat_id_daily_schedule[chat_id].goal = goal
    def set_daily_session(self, chat_id: int, day_session: DaySession):
        if chat_id not in self.chat_id_daily_schedule:
            self.chat_id_daily_schedule[chat_id] = DailyPlan()
        self.chat_id_daily_schedule[chat_id].day_session = day_session
    
    def set_day(self, chat_id: int, day: str):
        if chat_id not in self.chat_id_daily_schedule:
            self.chat_id_daily_schedule[chat_id] = DailyPlan()
        self.chat_id_daily_schedule[chat_id].day = day 
        logger.info(self.chat_id_daily_schedule[chat_id])
    def daily_scheduler(self, chat_id: int, user_name: str):
        
        try:
            self.chat_id_daily_schedule[chat_id].user_name = user_name
            self.chat_id_daily_schedule[chat_id].chat_id = chat_id

            if self.chat_id_daily_schedule[chat_id].get("task") is None and self.chat_id_daily_schedule[chat_id].get("goal") is None and self.chat_id_daily_schedule[chat_id].get("day_session") is None:
                return "You have not set any daily task, goal or session"
            else: 
                logger.info(self.chat_id_daily_schedule[chat_id])
                self.mongo_db.insert_one(collection_name=user_name, data = self.chat_id_daily_schedule[chat_id])
                return "Task scheduled successfully! 🎯"
        except:
            return "You have not set any daily task, goal or session"
    
    def scheduler(self, chat_id):
        columns = self.plan[chat_id].columns
        timeline = self.plan[chat_id][columns[0]]
        for i in range(len(timeline)):
            
            def do(index):
                
                time_str: str = timeline[index]
                start_time = time_str.split('-')[0]
                start_time_dt = DatetimeUtilities.str_to_datetime(dt_str=start_time, iso= False, fmt='%H:%M')
                prepare_time_dt = start_time_dt - datetime.timedelta(minutes=30)
                logger.info(f"Reminder set for: {prepare_time_dt.time().strftime('%H:%M')}")
                logger.info(f"Start time set for: {start_time_dt.time().strftime('%H:%M')}")
                def send_prepare():
                    task_reminder_first = f"Incomming 30 min: {self.get_task(index, chat_id)}"
                    self.callback_func(chat_id, task_reminder_first)
                def send_schedule():
                    task_reminder_at_time = f"Now: {self.get_task(index, chat_id)}"
                    self.callback_func(chat_id, task_reminder_at_time)


                schedule.every().day.at(prepare_time_dt.time().strftime('%H:%M')).do(send_prepare)
                schedule.every().day.at(start_time_dt.time().strftime('%H:%M')).do(send_schedule)

                schedule.run_pending()
            th = threading.Thread(target=do, args=[i,])
            th.daemon = True
            th.start()
        while True:
            schedule.run_pending()
            
        