import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment.settings')
django.setup()

from django.contrib.auth.models import User

# Reset password for testuser
try:
    user = User.objects.get(email='test@example.com')
    user.set_password('Password123')  # Set a known password
    user.save()
    print(f"✓ Password reset for {user.username} ({user.email})")
    print(f"  New password: Password123")
except User.DoesNotExist:
    print("User not found")

# Reset password for NavyaSri
try:
    user2 = User.objects.get(email='navyasrimuttha@gmail.com')
    user2.set_password('Password123')  # Set a known password
    user2.save()
    print(f"\n✓ Password reset for {user2.username} ({user2.email})")
    print(f"  New password: Password123")
except User.DoesNotExist:
    print("User not found")

print("\n=== You can now login with these credentials: ===")
print("Email: test@example.com")
print("Password: Password123")
print("\nOR")
print("Email: navyasrimuttha@gmail.com")
print("Password: Password123")
