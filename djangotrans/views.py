from django.shortcuts import render
from rest_framework.generics import *
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .customperm import AccountPermission
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'current_account': reverse('current_account', request=request, format=format),
        'saving_account': reverse('saving_account', request=request, format=format),
        'amount_with_draw': reverse('amount_with_draw', request=request, format=format),
    })


class View_Current_Account(viewsets.ModelViewSet):
    serializer_class = Cur_AccountSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        Accounts = Curr_Account.objects.filter(user=user)
        return Accounts


class View_Saving_Account(viewsets.ModelViewSet):
    serializer_class = Sav_AccountSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        Accounts = Saving_Account.objects.filter(user=user)
        return Accounts


class Sav_Account(viewsets.ModelViewSet):
    queryset = Saving_Account.objects.all()
    serializer_class = Sav_AccountSerializers
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]


class Currentt_Account(viewsets.ModelViewSet):
    queryset = Curr_Account.objects.all()
    serializer_class = Cur_AccountSerializers
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]


class Transfer_Amount(viewsets.ModelViewSet):
    queryset = Amount_Transfer.objects.all()
    serializer_class = AmountSerializers
    permission_classes = [IsAuthenticated]
    permission_classes = [AccountPermission]



class Amount_Withdraws_Details(viewsets.ModelViewSet):
    serializer_class = Withdraw_AmountSerializers
    permission_classes = [IsAuthenticated]
    permission_classes = [AccountPermission]

    def get_queryset(self):
        user = self.request.user
        Withdraw_details = Withdraw_Amount.objects.filter(user=user)
        return Withdraw_details