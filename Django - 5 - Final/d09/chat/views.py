from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room

@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
    })
