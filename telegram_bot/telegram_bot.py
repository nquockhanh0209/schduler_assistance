import os

from telebot import TeleBot

from commonkit.logging.logging_config import LogConfig
from config.config import Config
from schedule_handler import SchedulerHandler
log_config = LogConfig(__name__)
logger = log_config.logger
class TelegramBot:
    config: Config
    bot: TeleBot
    scheduler_handler: SchedulerHandler
    def __init__(self):

        self.config = Config()
        self.bot = TeleBot(self.config.BOT_TOKEN)
        self.scheduler_handler = SchedulerHandler(self.send_message)

    def send_message(self, chat_id: int, message: str):
        logger.info("callback called")
        
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
            "/monthly_plan - Upload your monthly plan in xlsx format\n"
            # Add more commands to the menu as needed
            )
            self.bot.send_message(message.chat.id, menu)

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.bot.reply_to(message, "Here is how you can use the bot...")

        @self.bot.message_handler(content_types=['monthly_plan'])
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
        self.bot.polling()
    

