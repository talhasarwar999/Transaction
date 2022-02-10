from rest_framework import permissions
from .models import *
class AccountPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        current_user = request.user
        Current_user_Account = Saving_Account.objects.filter(user=current_user).exists()
        Saving_user_Account = Curr_Account.objects.filter(user=current_user).exists()
        if Current_user_Account or Saving_user_Account:
            return True
        else:
            return False