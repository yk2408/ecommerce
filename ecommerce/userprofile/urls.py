
from django.urls import path, re_path
from . import views


urlpatterns = [
                path('register/', views.user_register, name='register'),
                path('login/', views.user_login, name='login'),
                path('logout/', views.user_logout, name='logout'),
                path('forgot-password/', views.forgot_password, name='forgot-password'),
                re_path(
                        r'reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
                        views.password_reset, name='reset-password'
                       ),
                path('myaccount/', views.my_account, name='myaccount'),
                path('manage-address', views.manage_address, name='manage-address'),
                path('add-address', views.add_address, name='add_address'),
                path('<int:id>/update-address', views.update_address, name='update-address'),
                path('<int:user_id>/delete-address', views.delete_address, name='delete-address'),
                path('my-order/', views.my_order, name='my-order'),
                path('my-order-details/<int:item_id>/<int:order_id>', views.my_order_details, name='my-order-details'),
                path('my-offer', views.my_offer, name='my-offer'),
                re_path(
                        r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
                        views.activate, name='activate'
                       ),
                path('subscribe/', views.subscribe_user, name='subscribe'),


              ]


