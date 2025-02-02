from commonkit.system_monitor.system_monitor import SystemMonitor
from telegram_bot.telegram_bot import TelegramBot


class App:
    telte_bot: TelegramBot
    def __init__(self):
        self.telte_bot = TelegramBot()
        self.telte_bot.start_bot()
        system_monitor = SystemMonitor()
        system_monitor.start()

if __name__ == '__main__':
    app = App()
