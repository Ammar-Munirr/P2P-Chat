from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import MyChat
from django.contrib.auth.decorators import login_required


User = get_user_model()


@login_required()
def index(request):
    frnd_name = request.GET.get('user')
    mychat_data = None
    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and MyChat.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)):
            frnd =  User.objects.get(username=frnd_name)
            mychat_data = MyChat.objects.filter(me=request.user,frnd=frnd)
    frnds = User.objects.exclude(id=request.user.id)
    return render(request,'index.html',{'my':mychat_data,'chats':mychat_data,'frnds':frnds})

