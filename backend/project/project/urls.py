
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [


    path('admin/', admin.site.urls),
    path('api/user/', include('accounts.urls')),
    path('api/chat/',include('chat.urls')),

    path('hotel/booking/', include('Booking.urls')),

    path('customadmin/', include('customadmin.urls')),

    path('api/', include('hotels.urls')),  
    
    path('notification/', include('notification.urls')),  
    path('chat/', include('chat.urls')),  



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


