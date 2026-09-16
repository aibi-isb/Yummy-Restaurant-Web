1. Customer Account (Verified Working)
Username: Ousi
Password: password123
Email: ousi@yummy.com
Role: Standard Customer

2. Admin / Superuser Account
Username: Tity
Email: tity@yummy.com
Role: Superuser / Admin (is_staff=True, is_superuser=True)
Password: aibi-tity!


# Reset password for the existing admin user:
./.venv/bin/python manage.py changepassword Tity

# Or create a new superuser:
./.venv/bin/python manage.py createsuperuser