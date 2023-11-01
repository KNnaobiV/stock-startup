from django.urls import path, include
import django.contrib.auth.urls
from authentik import views
from authentik.api.urls import urlpatterns as api_urls

app_name = 'authentik'

urlpatterns = [
]

urlpatterns += api_urls