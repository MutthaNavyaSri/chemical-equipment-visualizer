import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_equipment.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# List all users
print("=== All Users in Database ===")
for user in User.objects.all():
    print(f"Username: {user.username}, Email: {user.email}, Has usable password: {user.has_usable_password()}")

print("\n=== Testing Authentication ===")

# Test authentication with email
email = "test@example.com"
password = "Test123456"

try:
    user_obj = User.objects.get(email=email)
    print(f"Found user: {user_obj.username}")
    
    # Try to authenticate
    authenticated_user = authenticate(username=user_obj.username, password=password)
    
    if authenticated_user:
        print(f"✓ Authentication SUCCESS for {email}")
    else:
        print(f"✗ Authentication FAILED for {email}")
        print("  Password is incorrect or user is inactive")
except User.DoesNotExist:
    print(f"✗ User with email {email} does not exist")

print("\n=== Testing with another user ===")
email2 = "navyasrimuttha@gmail.com"
try:
    user_obj2 = User.objects.get(email=email2)
    print(f"Found user: {user_obj2.username}")
    print("  Try authenticating with the password you used during registration")
except User.DoesNotExist:
    print(f"✗ User with email {email2} does not exist")
