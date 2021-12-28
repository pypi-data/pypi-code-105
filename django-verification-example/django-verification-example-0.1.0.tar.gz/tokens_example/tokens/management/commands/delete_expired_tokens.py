from django.core.management.base import BaseCommand

from ...models import SecurityToken


class Command(BaseCommand):
    help = "Удалить просроченные экземпляры SecurityToken."

    def handle(self, *_, **__):
        self.stdout.write("Началось удаление просроченных экземпляров SecurityToken.")
        SecurityToken.objects.delete_expired()
        self.stdout.write("Удаление прошло успешно.")