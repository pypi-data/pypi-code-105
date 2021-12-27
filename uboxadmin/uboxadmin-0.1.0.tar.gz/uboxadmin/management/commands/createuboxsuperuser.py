from django.core.management.base import BaseCommand

from uboxadmin.models.system import User, UserRole


class Command(BaseCommand):
    help = "Used to create a superuser for ubox admin."

    def add_arguments(self, parser):
        """
        添加命令参数

        @param parser: see also: https://docs.python.org/3/library/argparse.html#module-argparse
        """
        parser.add_argument(
            "--username",
            required=True,
            type=str,
            help="Specifies the login for the superuser.",
        )
        parser.add_argument(
            "--password",
            required=True,
            type=str,
            help="Specifies the login for the superuser.",
        )

    def handle(self, *args, **options):
        user = User(username=options["username"])
        user.set_password(options["password"])
        user.save()
        UserRole.objects.update_or_create(
            user_id=User.objects.get(username=options["username"]).id,
            role_id=1,
        )
