from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', register, name="signup"),
    path('userpage/',userpage, name='userpage'),
    path('workerpage/',workerpage, name='workerpage'),
    path('providerpage/',providerpage, name='providerpage'),
    path('accounts/login/',signin),
    path('signin/signup', register ),
    path('signin/index', index ),
    path('userpage/userpage',userpage),
    path('workerpage/workerpage',workerpage),
    path('providerpage/providerpage',providerpage),
    path('signup/signin', signin ),
    path('signup/signup', register),
    path('signup/index', index ),
    path('signin/signin', signin ),   
    path('user_logout', views.user_logout, name='user_logout'),
    path('worker_logout', views.worker_logout, name='worker_logout'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('provider_logout', views.provider_logout, name='provider_logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('custom_admin_page/', views.custom_admin_page, name='custom_admin_page')
]