import os
from telebot import TeleBot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from commonkit.logging.logging_config import LogConfig
from config.config import Config
from schedule_handler import SchedulerHandler
from telebot import custom_filters
# Logger
log_config = LogConfig(__name__)
logger = log_config.logger

# Telegram Bot Class
class TelegramBot:
    def __init__(self):
        self.config = Config()
        self.bot = TeleBot(self.config.BOT_TOKEN)
        self.scheduler_handler = SchedulerHandler(self.send_message)
        # self.add_commands()

    def send_message(self, chat_id: int, message: str):
        logger.info("callback called")
        logger.info(f'send: {message}')
        self.bot.send_message(chat_id, message)
    
    def handle_messages(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            chat_id = message.chat.id
            text = message.text
            # Process the received message here
            print(f"Received message from {chat_id}: {text}")
        # handle_all_messages()
    def add_commands(self):

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, "Welcome to the bot! Use /help to see available commands.")

        @self.bot.message_handler(commands=['menu'])
        def send_menu(message):
            menu = (
                "/help - Show help message\n"
                "/menu - Show this menu\n"
                "/set_daily_task - Set your daily task\n"
                "/monthly_plan - Upload your monthly plan in xlsx format\n"
            # Add more commands to the menu as needed
            )
            self.bot.send_message(message.chat.id, menu)

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.bot.reply_to(message, "Here is how you can use the bot...")

        g_state = None
        @self.bot.message_handler(commands=['set_daily_task'])
        def handle_daily_task(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            msg = self.bot.send_message(message.chat.id, "What task do you plan today?")
            self.bot.register_next_step_handler(msg, receive_task)

        
        def receive_task(message):
            print(f"🔵 receive_task() called for {message.from_user.id}")
            task = message.text
            self.scheduler_handler.set_daily_task(chat_id=message.chat.id, task=task)
            msg = self.bot.send_message(message.chat.id, "Received task\nWhat is the task for your big goal?")
            self.bot.register_next_step_handler(msg, receive_goal)

        # @self.bot.message_handler(state=DailyTaskState.goal)
        def receive_goal(message):
            goal = message.text
            self.scheduler_handler.set_goal(chat_id=message.chat.id, goal=goal)
            msg = self.bot.send_message(message.chat.id, "Received goal\nWhich session would you plan to do this task?\n(morning, afternoon, or evening?)")
            self.bot.register_next_step_handler(msg, receive_session)


        # @self.bot.message_handler(state=DailyTaskState.day_session)
        def receive_session(message):
            day_session = message.text
            self.scheduler_handler.set_daily_session(chat_id=message.chat.id, day_session=day_session)
            msg = self.bot.send_message(message.chat.id, "What day are you going to do this task?")
            self.bot.register_next_step_handler(msg, receive_day)

        # @self.bot.message_handler(state=DailyTaskState.day)
        def receive_day(message):
            day = message.text
            self.scheduler_handler.set_day(chat_id=message.chat.id, day=day)
            msg = self.scheduler_handler.daily_scheduler(chat_id=message.chat.id, user_name=message.from_user.username)
            self.bot.send_message(message.chat.id, msg)

        @self.bot.message_handler(content_types=['document'])
        def handle_xlsx_file(message):
            sender = message.from_user.username
            chat_id = message.chat.id
            if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                file_info = self.bot.get_file(message.document.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)
                folder_path = './files'
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                file_path = os.path.join(folder_path, message.document.file_name)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                self.scheduler_handler.save_chat_id_schedule_to_csv(sender = sender, chat_id=chat_id, file_name=file_path)
                self.scheduler_handler.create_user_schedule(chat_id=chat_id, file_name=file_path)
                self.bot.reply_to(message, "File received and saved successfully.")
            else:
                self.bot.reply_to(message, "Please send an xlsx file.")
        # Add more command handlers as needed
  
    def start_bot(self):
        print("Starting bot...")
        
        self.add_commands()
        self.handle_messages()
        self.bot.polling(none_stop=True, interval=0)
    

