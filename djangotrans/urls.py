from django.urls import path
from .import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *#CreateOrder, api_root


current_account = View_Current_Account.as_view({
    'get': 'list',
})
saving_account = View_Saving_Account.as_view({
    'get': 'list',
})
amount_with_draw = Amount_Withdraws_Details.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('current_account/', current_account, name='current_account'),
    path('saving_account/', saving_account, name='saving_account'),
    path('amount_with_draw/', amount_with_draw, name='amount_with_draw'),

])