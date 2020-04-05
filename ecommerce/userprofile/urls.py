"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from . import views


urlpatterns = [
                path('register/', views.user_register, name='register'),
                path('login/', views.user_login, name='login'),
                path('logout/', views.user_logout, name='logout'),
                path('myaccount/', views.my_account, name='myaccount'),
                path('manage-address', views.manage_address, name='manage-address'),
                path('add-address', views.add_address, name='add_address'),
                path('<int:id>/update-address', views.update_address, name='update-address'),
                path('<int:user_id>/delete-address', views.delete_address, name='delete-address'),
                re_path(
                        r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
                        views.activate, name='activate'
                       ),
                path('subscribe/', views.subscribe_user, name='subscribe'),

              ]


