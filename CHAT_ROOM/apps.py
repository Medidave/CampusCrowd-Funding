from django.apps import AppConfig


class ChatRoomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CHAT_ROOM'

    def ready(self):

        import CHAT_ROOM.signals
