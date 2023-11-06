from django.urls import path, include
import django.contrib.auth.urls
from authentik import views
from authentik.api.urls import urlpatterns as api_urls

app_name = 'authentik'

urlpatterns = [
    path('login/', views.DefaultLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls'),),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/<str:username>', views.Profile.as_view(), name='profile'),
    path('trade/<uuid:uuid>/', views.TradeDetailView.as_view(), name='trade-detail'),
    path('trade/list/', views.TradeListView.as_view(), name='trade-list'),
    path('portfolio/<int:id>', views.portfolio_pnl, name='portfolio_pnl')
]

urlpatterns += api_urls