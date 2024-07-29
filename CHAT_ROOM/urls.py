from django.urls import path
from . import views


urlpatterns = [
    path('chat-room/', views.chatRoom, name='chat-room'),
    path('special-login/<str:pk>', views.specialLogin, name='special-login'),
    path('the-room/<str:pk>/', views.church_chat_room, name='church-chat-room'),
    # path('search_topic/', views.search_topic, name='search_topic'),

]