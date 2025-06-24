from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Créer un utilisateur administrateur par défaut'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Nom d\'utilisateur (défaut: admin)')
        parser.add_argument('--password', type=str, default='admin123', help='Mot de passe (défaut: admin123)')
        parser.add_argument('--email', type=str, default='admin@example.com', help='Email (défaut: admin@example.com)')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'L\'utilisateur "{username}" existe déjà.')
            )
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='ADMIN'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Utilisateur administrateur créé avec succès!\n'
                f'Nom d\'utilisateur: {username}\n'
                f'Mot de passe: {password}\n'
                f'Email: {email}\n'
                f'Rôle: Administrateur'
            )
        )
