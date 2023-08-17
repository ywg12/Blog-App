from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Delete a user by ID'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID of the user to delete')

    def handle(self, *args, **options):
        user_id = options['user_id']
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted user with ID {user_id}'))
        except:
            self.stdout.write(self.style.ERROR('Could not delete user'))
