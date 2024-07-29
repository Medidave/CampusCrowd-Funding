from django.urls import path
from .import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    # path('signUp', views.signUp, name='signUp'),
    path('logout', views.logout_view, name='logout'),
    path('edit-profile', views.editProfile, name='edit-profile'),
    path('view-profile/<str:pk>/', views.view_profile, name='view_profile'),
    path('update-project/<str:pk>/', views.updateProject, name='updateProject'),
    path('create-project/<str:pk>/', views.createProject, name='createProject'),
    path('update-project-detail/<str:pk>/', views.updateProjectDetail, name='updateProjectDetail'),
    path('create-project-detail/<str:pk>/', views.createProjectDetail, name='createProjectDetail'),
    path('send_mail/<str:pk>/', views.send_mail, name='send_mail'),
    path('suggestions/<str:pk>/', views.suggestions, name='suggestions'),

]