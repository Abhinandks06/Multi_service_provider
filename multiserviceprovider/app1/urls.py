from django.urls import path
from .views import *
from . import views
from .views import CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetConfirmView,CustomPasswordResetCompleteView
urlpatterns = [
    path('', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', register, name="signup"),
    path('userpage/',userpage, name='userpage'),
    path('userpage/services',services, name='services'),
    path('workerpage/',workerpage, name='workerpage'),
    path('providerpage/',providerpage, name='providerpage'),
    path('accounts/login/signin',signin),
    path('accounts/login/',signin),
    path('signin/signup', register ),
    path('signin/index', index ),
    path('userpage/userpage',userpage),
    path('workerpage/workerpage',workerpage),
    path('providerpage/providerpage',providerpage),
    path('signup/signin', signin ),
    path('accounts/login/signup', register ),
    path('accounts/login/index', index ),      
    path('signup/signup', register),
    path('signup/index', index ),
    path('signin/signin', signin ),   
    path('user_logout', views.user_logout, name='user_logout'),
    path('worker_logout', views.worker_logout, name='worker_logout'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('provider_logout', views.provider_logout, name='provider_logout'),
    path('resetpassword/', CustomPasswordResetView.as_view(), name='resetpassword'),
    path('resetpassword/done/',CustomPasswordResetDoneView.as_view(),name='resetpassworddone'),
    path('resetpassword/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='resetpasswordconfirm'),
    path('resetpassword/complete',CustomPasswordResetCompleteView.as_view(),name='passwordresetcomplete'),
    path('custom_admin_page/', views.custom_admin_page, name='custom_admin_page'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    
]