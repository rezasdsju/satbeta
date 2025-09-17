from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # <-- home.urls include আছে কি check করো
    path('data/', include('data.urls')),
]
