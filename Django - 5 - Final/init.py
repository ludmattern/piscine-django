import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')
django.setup()

from django.contrib.auth.models import User
from d09.chat.models import Room

users = ['pim', 'pam', 'poum']
password = 'password'

for username in users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)
        print(f"User {username} created.")
    else:
        print(f"User {username} already exists.")

rooms = ["Pim's Pitiful Pit of Despair", "Pam's Pathetic Playground of Shame", "Poum's Pitiable Palace of Losers"]

for room_name in rooms:
    if not Room.objects.filter(name=room_name).exists():
        Room.objects.create(name=room_name)
        print(f"Room {room_name} created.")
    else:
        print(f"Room {room_name} already exists.")
