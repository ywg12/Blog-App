from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update first name and last name for users'

    def handle(self, *args, **options):
        updated_user_data = [
            # {'id': 1, 'first_name': 'Yash', 'last_name': 'Gaur'},
            # {'id': 2, 'first_name': 'John', 'last_name': 'Smith'},
            {'id': 3, 'first_name': 'Aman', 'last_name': 'Khan'},
            {'id': 4, 'first_name': 'Anshuman', 'last_name': 'Sharma'},
            {'id': 5, 'first_name': 'Ritesh', 'last_name': 'Sharma'}
            
        ]

        
        users_to_update = [
            User(id=user['id'], first_name=user['first_name'], last_name=user['last_name'])
            for user in updated_user_data
        ]

        User.objects.bulk_update(users_to_update, ['first_name', 'last_name'])

        self.stdout.write(self.style.SUCCESS('Successfully updated user names'))
