from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum, F
from django.db.models.functions import TruncMinute
from django.http import JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from authentik.services.forms import *
from authentik.models  import *


User = get_user_model()

def portfolio_pnl(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    pnl = portfolio.pnl()
    data = {"data": {"pnl": pnl, "time": portfolio.time.strftime("%m/%d %H:%M:%S")}}
    return JsonResponse(data)


class DefaultLoginView(LoginView):
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse(
            'authentik:profile', 
            kwargs={'username': self.request.user.username,}
        )


class Register(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'registration/register.html'


class Profile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'authentik/profile.html'
    context_object_name = 'user'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        portfolio = Portfolio.objects.filter(trader=self.request.user)
        if portfolio:
            context["portfolio"] = portfolio
        if self.request.user.is_manager:
            context["user_list"] = User.objects.filter(supervisor=self.request.user)
        if not self.request.user.is_manager:
            context["trade_list"] = Trade.objects.filter(portfolio__trader=self.request.user)
        return context


class TradeDetailView(LoginRequiredMixin, DetailView):
    model = Trade
    template_name = 'authentik/trade_detail.html'
    context_object_name = 'trade'
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class TradeListView(LoginRequiredMixin, ListView):
    model = Trade
    template_name = 'authentik/trade_list.html'
    context_object_name = 'trades'
    def get_queryset(self):
        return Trade.objects.filter(portfolio__trader=self.request.user)