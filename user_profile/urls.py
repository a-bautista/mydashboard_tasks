from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# import the component task
from .views import view_user_settings, view_app_settings

urlpatterns = [
    path('user/', view_user_settings, name='user_settings'),
    path('app_settings/', view_app_settings, name='app_settings')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)