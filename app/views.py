from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import MyChat

User = get_user_model()


@login_required()
def chat(request, id):
    frnd_name = id
    mychats_data = None
    if frnd_name:
        if User.objects.filter(id=frnd_name).exists() and MyChat.objects.filter(me=request.user, frnd=User.objects.get(id=frnd_name)).exists():
            frnd_ = User.objects.get(id=frnd_name)
            mychats_data = MyChat.objects.get(me=request.user, frnd=frnd_).chat
    frnds = User.objects.exclude(pk=request.user.id)
    return render(request, "index.html", {"my": mychats_data, "frnd_id": frnd_name, "chats": mychats_data, "frnds": frnds})


@login_required
def users(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, "users.html", {"users": users})
