from django.core.management.base import BaseCommand
from bot import bot_handler

class Command(BaseCommand):
    def handle(self, *args, **options):
        bot_handler.main()
        