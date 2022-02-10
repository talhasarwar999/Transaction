from rest_framework import serializers
from .models import *
from rest_framework.fields import CurrentUserDefault
from django.http import HttpResponseRedirect
from datetime import date
from django.contrib.auth.models import User
from django.db import transaction
import copy


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class Sav_AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Saving_Account
        fields = ['id','user','acc_name','acc_no','your_name','address','amount','mobile','city','desc','created','update']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = UserSerializers(instance.user).data
        return rep

    def save(self, **kwargs):
        reqs_user = self.context['request'].user
        gets = Saving_Account.objects.filter(user=reqs_user).last()
        old_data = [gets.user,gets.acc_name,gets.acc_no,gets.your_name,gets.address,gets.amount,gets.mobile,gets.city,
                        gets.desc,gets.created,gets.update]
        new_copeid = copy.copy(old_data)
        old_data.append('talha')
        print(old_data)
        print(new_copeid)



class Cur_AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curr_Account
        fields = ['id','user','acc_name','acc_no','your_name','address','amount','mobile','city','desc','created','update']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = UserSerializers(instance.user).data
        return rep

    # def save(self, **kwargs):
    #     reqs_user = self.context['request'].user
    #     get_list = []
    #     gets = Curr_Account.objects.filter(user=reqs_user).last()
    #     old_data = [gets.user,gets.acc_name,gets.acc_no,gets.your_name,gets.address,gets.amount,gets.mobile,gets.city,
    #                     gets.desc,gets.created,gets.update]
    #     print(old_data)
    #     copeid = copy.deepcopy(old_data)
    #     old_data[0] = 'Talha Sarwar'
    #     print(copeid)


class Withdraw_AmountSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Withdraw_Amount
        fields = ['id','user','your_name','type','acc_name','acc_no','withdraw_amount','withdraw_date']

    def create(self, validated_data):
            with transaction.atomic():
                reqs_user = self.context['request'].user
                your_name = self.validated_data['your_name']
                acc_name = self.validated_data['acc_name']
                acc_no = self.validated_data['acc_no']
                type = self.validated_data['type']
                withdraw_amount = self.validated_data['withdraw_amount']
                if type == "Current":
                    gets = Curr_Account.objects.get(user=reqs_user, your_name=your_name, acc_name=acc_name, acc_no=acc_no)
                    gets.amount -= int(withdraw_amount)
                    gets.save()
                else:
                    gets = Saving_Account.objects.get(user=reqs_user, your_name=your_name, acc_name=acc_name, acc_no=acc_no)
                    if (date.today() - gets.created).days < 180:
                        loss = withdraw_amount * 5 / 100
                        gets.amount -= loss
                        gets.save()
                        gets.amount -= int(withdraw_amount)
                        gets.save()
                    elif (date.today() - gets.created).days > 180 and (date.today() - gets.created).days < 365:
                        withdraw = Withdraw_Amount.objects.filter(user=reqs_user, type='Saving').last()
                        if withdraw:
                            if (date.today() - withdraw.withdraw_date).days > 180 and (date.today() - withdraw.withdraw_date).days < 365:
                                interest = withdraw_amount * 5 / 100
                                gets.amount += interest
                                gets.save()
                                gets.amount -= int(withdraw_amount)
                                gets.save()
                            else:
                                loss = withdraw_amount * 5 / 100
                                gets.amount -= loss
                                gets.save()
                                gets.amount -= int(withdraw_amount)
                                gets.save()
                        else:
                            interest = withdraw_amount * 5 / 100
                            gets.amount += interest
                            gets.save()
                            gets.amount -= int(withdraw_amount)
                            gets.save()
                    elif (date.today() - gets.created).days > 365:
                        withdraw = Withdraw_Amount.objects.filter(user=reqs_user, type='Saving').last()
                        if withdraw:
                            if (date.today() - withdraw.withdraw_date).days > 180 and (date.today() - withdraw.withdraw_date).days < 365:
                                interest = withdraw_amount * 5 / 100
                                gets.amount += interest
                                gets.save()
                                gets.amount -= int(withdraw_amount)
                                gets.save()
                            elif (date.today() - withdraw.withdraw_date).days > 365    :
                                interest = withdraw_amount * 10 / 100
                                gets.amount += interest
                                gets.save()
                                gets.amount -= int(withdraw_amount)
                                gets.save()
                            else:
                                loss = withdraw_amount * 5 / 100
                                gets.amount -= loss
                                gets.save()
                                gets.amount -= int(withdraw_amount)
                                gets.save()
                        else:
                            interest = withdraw_amount * 10 / 100
                            gets.amount += interest
                            gets.save()
                            gets.amount -= int(withdraw_amount)
                            gets.save()
                return Withdraw_Amount.objects.create(**validated_data)



class AmountSerializers(serializers.ModelSerializer):
    request_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=False)
    class Meta:
        model = Amount_Transfer
        fields = ['id','request_user','user','trans_amount']

    def save(self, **kwargs):
            with transaction.atomic():
                reqs_user = self.context['request'].user
                user = self.validated_data['user']
                trans_amount = self.validated_data['trans_amount']
                gets = Saving_Account.objects.get(user=reqs_user)
                gets.amount -= int(trans_amount)
                gets.save()
                gett = Saving_Account.objects.get(user=user)
                gett.amount += int(trans_amount)
                gett.save()
            return HttpResponseRedirect(redirect_to='account')










