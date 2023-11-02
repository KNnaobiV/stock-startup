from rest_framework import permissions

__all__ = [
    "CanViewTradeDetail",
    "CanViewTradeList",
]

class CanViewTradeDetail(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.portfolio.trader or request.user == obj.portfolio.trader.supervisor

class CanViewTradeList(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user == view.portfolio.trader or request.user == view.portfolio.trader.supervisor