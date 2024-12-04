'''from django.db import models
from bot_app.main import bot

class Notification(models.Model):
    user_id = models.IntegerField()  # Telegram user ID
    message = models.TextField()

    def send_notification(self):
        # Use Aiogram to send a message
        bot.loop.create_task(bot.send_message(self.user_id, self.message))'''
