"""DjangoTransaction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from djangotrans import views

router = DefaultRouter()
router.register('current_account_for_admin',views.Currentt_Account,basename='cur_account')
router.register('saving_account_for_admin',views.Sav_Account,basename='sav_account')
router.register('transfer_amount',views.Transfer_Amount,basename='transfer_amount')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('accounts/', include('djangotrans.urls')),
    path('auth/', include('rest_framework.urls',namespace="rest_framework")),
]
