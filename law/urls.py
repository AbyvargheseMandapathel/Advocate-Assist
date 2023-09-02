# law/urls.py
from django.contrib import admin
from django.urls import path, include 
from accounts import views# Import the include function
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('allauth.urls')),
    path('error/', views.error, name='error'),
    

    # path('lawyer/<int:lawyer_id>/', views.lawyer_details, name='lawyer_details'),

    # Add other URL patterns for your project
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
