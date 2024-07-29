from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all-campaigns', views.all_campaigns, name='campaigns'),
    path('create-campaigns', views.create_campaign, name='create-campaigns'),
    path('edit-campaigns/<str:pk>/', views.edit_campaign, name='edit_campaign'),
    path('campaign/<str:pk>/', views.campaign, name='campaign'),
    path('perks/<str:pk>/', views.perks, name='perks'),
    path('updates/<str:pk>/', views.updates, name='updates'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('about_us', views.about_us, name='about_us'),
    path('like_project/<str:pk>/', views.like_project, name='like_project'),
    path('initiate/<str:project_id>/', views.initiate_payment, name='initiate'),
    path('verify/<str:reference>/', views.verify_payment, name='verify'),
    path('sort_campaigns/<str:value>/', views.sort_campaigns, name='sort_campaigns'),
    path('search_projects', views.search_projects, name='search_projects'),
    path('hints/<str:pk>/', views.hints, name='hints'),
]