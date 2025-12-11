from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a new user with specified role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('--email', type=str, default='', help='Email address')
        parser.add_argument('--role', type=str, choices=['ADMIN', 'SALES'], default='SALES', 
                          help='User role (ADMIN or SALES)')
        parser.add_argument('--password', type=str, help='Password (will prompt if not provided)')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        role = options['role']
        password = options.get('password')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User "{username}" already exists'))
            return

        if not password:
            password = input('Password: ')
            password_confirm = input('Password (again): ')
            if password != password_confirm:
                self.stdout.write(self.style.ERROR('Passwords do not match'))
                return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {role} user: {username}'
        ))
