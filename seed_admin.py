import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

def seed_superuser():
    User = get_user_model()
    
    # Read credentials from environment variables, or use defaults
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    if not User.objects.filter(username=username).exists():
        print(f"Seeding admin user: {username}")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Admin user created successfully.")
    else:
        print(f"Admin user '{username}' already exists. Skipping.")

if __name__ == '__main__':
    seed_superuser()
