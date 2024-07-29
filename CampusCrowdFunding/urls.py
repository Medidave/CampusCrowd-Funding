
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('CampusCrowd.urls')),
    path('users/', include('users.urls')),
    path('CHAT_ROOM/', include('CHAT_ROOM.urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# Configure admin titles
admin.site.site_header = "CampusCrowd"
admin.site.site_title = "CampusCrowd"