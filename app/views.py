from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import MyChat
from django.contrib.auth.decorators import login_required


User = get_user_model()


@login_required()
def index(request):
    frnd_name = request.GET.get('user',None)
    mychats_data = None
    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and MyChat.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = MyChat.objects.get(me=request.user,frnd=frnd_).chat
    frnds = User.objects.exclude(pk=request.user.id)
    return render(request,'index.html',{'my':mychats_data,'chats': mychats_data,'frnds':frnds})

