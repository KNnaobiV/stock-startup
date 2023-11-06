from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from authentik.api.views import *

router = DefaultRouter()

urlpatterns = [
    path("change_password/<int:pk>/", ChangePasswordView.as_view(), name="change_password"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout_all/", LogoutAllView.as_view(), name="logout_all"),
    path("portfolio/<int:pk>/", PortfolioDetailAPI.as_view(), name="portfolio_detail"),
    #path('portfolio_pnl/<int:portfolio_id>/', views.portfolio_pnl, name='portfolio_pnl'),
    path("register/", RegisterView.as_view(), name="register"),
    path("trade/create/", TradeCreateAPI.as_view(), name="trade_create"),
    path("trade/list/", TradeListAPI.as_view(), name="trade_list"),
    path("trade/<uuid:uuid>/", TradeDetailAPI.as_view(), name="trade_detail"),
    path("update_profile/<int:pk>/", UpdateProfileView.as_view(), name="update_profile"),
]
