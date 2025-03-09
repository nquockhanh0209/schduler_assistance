from datetime import time
import datetime
import pandas as pd
import schedule
from commonkit.utilities.datetime_utilities import DatetimeUtilities
from schedule_handler import SchedulerHandler
from telegram_bot.telegram_bot import TelegramBot
# # import schedule
# # import time
from telebot import TeleBot
# bot = TeleBot("7499935883:AAFlo8OPnPWeFbrVUwthNh8P774jUsFQZsY")
# # chat_id = bot.get_chat()
# # ("@khanhv0209")
# bot.send_message(chat_id=5569919949, text="khanhv0209")
# # print(chat_id)
# while True: pass
# handler = SchedulerHandler()
# handler.sender_schedule['khanh'] = './files/Daily plan.xlsx'
# handler.convert_xlsx_to_df('khanh')
# print(handler.plan['khanh']["Unnamed: 0"][0])
# # def job():
# #     handler.convert_xlsx_to_df('khanh')
# #     print(handler.plan['khanh']['Monday'][16])

# # schedule.every().day.at("01:00").do(job)

# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)
# def start_all_schedules():
#     all_schdule_df = pd.DataFrame(pd.read_csv('/home/khanhv/code/scheduler/files/database/database.csv'))
#     for row in all_schdule_df.iterrows():
#         chat_id = row[1]['chat_id']
#         sender = row[1]['sender']
#         file_name = row[1]['file_name']
#         print(f'{chat_id} {sender} {file_name}')

# start_all_schedules()

start_time_dt = DatetimeUtilities.str_to_datetime(dt_str="07:00", iso= False, fmt='%H:%M')
print(start_time_dt.time().strftime('%H:%M'))
reminder_time_dt = start_time_dt - datetime.timedelta(minutes=30)
print(f"Reminder set for: {reminder_time_dt.time().strftime('%H:%M')}")
        