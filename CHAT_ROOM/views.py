from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib import messages 
from .forms import ReplyForm, MessageForm
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout 
from users.models import Profile
from django.db.models import Q



# Create your views here.
def chatRoom(request):
    rooms = Chat_forum.objects.all()
    # participants_count = rooms.participants.all()
    room_count = rooms.count()
    has_rooms = True

    context = {
        'rooms': rooms,
        'room_count': room_count,
        'has_rooms': has_rooms,
    }

    return render(request, 'CHAT_ROOM/let_us_start_eh.html', context)


def specialLogin(request, pk):
    page = 'login'
    room_id = pk

    if request.method == 'POST':
        username = request.POST['username']    # .lower() this was causing a problem in my login that is why i commented it 
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        
        except:
            messages.error(request, "Your username is incorrect or does not exist!!!")
        
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            url = reverse('church-chat-room', kwargs={'pk': pk})
            return redirect(url)
        else:
            messages.error(request, "Your password is incorrect please login again!!!")

        context = {
            'page': page,
            'room_id': room_id
            }
    return render(request, 'account/login.html')



# @login_required(login_url='login')
def church_chat_room(request, pk):
    if (not request.user.is_authenticated):
        messages.error(request, "Please login into your account to be able to engage in a chat")
        return redirect('special-login', pk=pk)

    project = Project.objects.get(id=pk)
    room = Chat_forum.objects.get(project=project)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    rooms = Chat_forum.objects.all()

    try:
        is_participant_present = room.participants.get(id=request.user.profile.id)
    except Profile.DoesNotExist:
        is_participant_present = False
        pass
    else:
        pass

    if not is_participant_present:
        room.participants.add(request.user.profile)


    if request.method == "GET":
        query = request.GET.get('browse_topics') if request.GET.get('browse_topics') != None else ''
        # rooms = Chat_forum.objects.filter(topic__name__icontains=query)


    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, 'Please log into your account to be able to chat')
            return redirect('login')

        if 'image' in request.FILES:  # Using a form would access data through form.cleaned_data
            image_file = request.FILES['image']
        else:
            image_file = ""

        message = Message.objects.create(
           user = request.user.profile,
           room=room,
           body=request.POST.get('message'),
           image=image_file
       )
        room.participants.add(request.user.profile)
        return redirect('church-chat-room', pk=room.id)
        

    base_url = request.build_absolute_uri('/')  # Get the base URL from the request   

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'rooms': rooms,
        'is_chat_room': True,
        'base_url': base_url,
        'project': project,
    }

    
    return render(request, 'CHAT_ROOM/chat_room.html', context)

# web: gunicorn THE_LOVE_SUNCTUARY.wsgi --log-file -
