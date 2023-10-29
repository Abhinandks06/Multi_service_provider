from django.urls import path , include
from .views import *
from . import views
from .views import CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetConfirmView,CustomPasswordResetCompleteView
urlpatterns = [
    path('', index, name="index"),
    path('provider_reg/', provider_reg, name="provider_reg"),
    path('worker_reg/', worker_reg, name="worker_reg"),
    path('signin/', signin, name="signin"),
    path('signup/', register, name="signup"),
    path('providersignup/', providerregister, name="providersignup"),
    path('workersignup/', workerregister, name="workersignup"),
    path('userpage/',userpage, name='userpage'),
    path('userpage/providerlist',providerlist, name='providerlist'),
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
    path('accounts/', include('allauth.urls')),
    path('custom_admin_page/provider_registration/', views.provider_registration, name='provider_registration'),
    path('providerpage/worker_registration/', views.worker_registration, name='worker_registration'),
    #here google starts
    path('auth/', include('social_django.urls', namespace='social')),
    path("", include("allauth.urls")),
    #here google ends
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
    path('worker_registration/', views.worker_registration, name='worker_registration'),
    path('providerpage/worker_registration/', views.worker_registration, name='worker_registration'),
    path('worker_reg/register/', views.worker_registration, name='worker_registration'),
     path('service/<str:category>/', views.service_providers_by_category, name='service_providers_by_category'),
     path('update_profile/', views.update_profile, name='update_profile'),
    
]