from django.db import models
from asgiref.sync import sync_to_async





''' этот код определяет модель уведомления в Django, которая может хранить идентификатор пользователя Telegram и текст сообщения. 
Метод send_notification позволяет отправлять уведомления пользователю через Telegram, используя библиотеку Aiogram. 
Это может быть полезно для создания системы уведомлений в приложении, где пользователи могут получать сообщения через Telegram'''


class Notification(models.Model):
    user_id = models.IntegerField(null=False)  # Telegram user ID
    message = models.TextField()

    # метод, который будет использоваться для отправки уведомления пользователю Telegram.
    '''def send_notification(self):
            bot.loop.create_task(bot.send_message(self.user_id, self.message))'''


# Асинхронная функция для получения данных из базы данных
@sync_to_async
def get_users_to_sending_message_from_db():
    return list(Notification.objects.all())

@sync_to_async
def delete_user(user):
    user.delete()