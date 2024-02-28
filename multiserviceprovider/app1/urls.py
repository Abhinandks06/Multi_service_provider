from django.urls import path , include
from .views import *
from . import views
from .views import CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetConfirmView,CustomPasswordResetCompleteView
urlpatterns = [
    path('', index, name="index"),
    path('provider_reg/', provider_reg, name="provider_reg"),
    path('provider_reg/signin', signin, name="signin"),
    path('worker_reg/', worker_reg, name="worker_reg"),
    path('worker_reg/signin', signin, name="signin"),
    path('worker_reg/index', index, name="index"),
    path('provider_reg/index', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', register, name="signup"),
    path('providersignup/', providerregister, name="providersignup"),
    path('workersignup/', workerregister, name="workersignup"),
    path('signin/userpage/',userpage, name='userpage'),
    path('signin/userpage/userpage',userpage, name='userpage'),
    path('userpage/',userpage, name='userpage'),
    path('signin/userpage/user_logout',user_logout),
    path('search_providers/userpage.html',userpage, name='userpage'),
    path('search_providers/userpage',userpage, name='userpage'),
    path('userpage/providerlist',providerlist, name='providerlist'),
    path('userpage/providerlist/book_service',book_service, name='book_service'),
    path('userpage/providerlist/book_service/<int:userid>/', book_service, name='book_service'),
    path('workerpage/',workerpage, name='workerpage'),
    path('worker_requests/workerpage',workerpage, name='workerpage'),
    path('providerpage/',providerpage, name='providerpage'),
    path('bookinghistory/managerpage/',managerpage, name='managerpage'),
    path('bookinghistory/providerpage/providerpage',providerpage, name='providerpage'),
    path('accounts/login/signin',signin),
    path('accounts/login/',signin),
    path('signin/signup', register ),
    path('signin/index', index ),
    path('userpage/userpage',userpage),
    path('search/userpage',userpage),
    path('service/Cleaning/userpage',userpage),
    path('create_booking/userpage',userpage),
    path('service/Cleaning/userpage.html',userpage),
    path('service/Laundry/userpage',userpage),
    path('service/Laundry/userpage.html',userpage),
    path('service/Repair/userpage',userpage),
    path('service/Plumbing/userpage',userpage),
    path('service/Repair/userpage.html',userpage),
    path('service/Plumbing/userpage.html',userpage),
    path('service/Electrical/userpage.html',userpage),
    path('service/Electrical/userpage',userpage),
    path('service/Pestcontrol/userpage.html',userpage),
    path('service/Plumbing/user_logout',user_logout),
    path('service/Repair/user_logout',user_logout),
    path('service/Cleaning/user_logout',user_logout),
    path('service/Pestcontrol/user_logout',user_logout),
    path('service/Laundry/user_logout',user_logout),
    path('service/Electrical/user_logout',user_logout),
    path('workerpage/workerpage',workerpage),
    path('providerpage/providerpage',providerpage),
    path('signup/signin', signin ),
    path('accounts/login/signup', register ),
    path('accounts/login/index', index ),      
    path('signup/signup', register),
    path('signup/index', index ),
    path('signin/signin', signin ),   
    path('signin/user_logout', views.user_logout, name='user_logout'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('userpage/user_logout', views.user_logout, name='user_logout'),
    path('userpage/providerlist/user_logout', views.user_logout, name='user_logout'),
    path('worker_logout', views.worker_logout, name='worker_logout'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('provider_logout', views.provider_logout, name='provider_logout'),
    path('manager_logout', views.manager_logout, name='manager_logout'),
    path('resetpassword/', CustomPasswordResetView.as_view(), name='resetpassword'),
    path('resetpassword/done/',CustomPasswordResetDoneView.as_view(),name='resetpassworddone'),
    path('resetpassword/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='customresetpasswordconfirm'),
    path('resetpassword/complete',CustomPasswordResetCompleteView.as_view(),name='passwordresetcomplete'),
    path('custom_admin_page/', views.custom_admin_page, name='custom_admin_page'),
    path('activate_user/<int:userid>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:userid>/', views.deactivate_user, name='deactivate_user'),
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
     path('update_profile/user_logout', views.user_logout, name='user_logout'),
     path('view_profile/user_logout', views.user_logout, name='user_logout'),
     path('view_profile/', views.profile_view, name='view_profile'),
     path('update_profile/userpage.html',userpage, name='userpage'), 
     path('view_profile/userpage.html',userpage, name='userpage'), 
     path('view_profile/userpage.html',userpage, name='userpage'), 
     path('userpage/providerlist/userpage',userpage, name='userpage'), 
     path('userpage/providerlist/userpage.html',userpage, name='userpage'), 
     path('social-auth/', include('social_django.urls', namespace='social-auth')),
     path('google-profile-update/<str:username>/<str:email>/', views.google_profile_update, name='google_profile_update'),
     path('userpage/google-profile-update/<str:username>/<str:email>/', views.google_profile_update, name='google_profile_update'),
     path('custom_admin_page/requests/', views.admin_requests, name='admin_requests'),
     path('providerpage/requests/', views.worker_requests, name='worker_requests'),
     path('custom_admin_page/requests/custom_admin_page', views.custom_admin_page, name='custom_admin_page'),
     path('custom_admin_page/activate_provider/<int:user_id>/', views.activate_provider, name='activate_provider'),
     path('providerpage/workerrequests/activate_worker/<int:user_id>/', views.activate_worker, name='activate_worker'),
     path('providerpage/activate_worker/<int:userid>/', views.activate_worker, name='activate_worker'),
     path('providerpage/providerrequests/providerpage', views.providerpage, name='providerpage'),
     path('providerpage/providerrequests/workerpage', views.providerpage, name='providerpage'),
     path('create_booking/', create_booking, name='create_booking'),
     path('search/', views.search_providers, name='search_providers'),
     path('search_providers/', views.search_providers, name='search_providers'),
     path('bookservice/<int:userid>/', views.render_booking_form, name='render_booking_form'),
     path('approve_booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
     path('reject_booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
     path('provider_bookings/', views.provider_bookings, name='provider_bookings'),
     path('provider_bookings/providerpage', views.providerpage, name='providerpage'),
     path('bookinghistory/', views.bookinghistory, name='bookinghistory'),
     path('approve_booking/providerpage',providerpage),
     path('worker_requests/<int:user_id>', views.worker_requests, name='worker_requests'),
     path('approve_worker/<int:user_id>/', views.activate_worker, name='approve_worker'),
     path('providerpage/approve_worker/<int:user_id>/', views.activate_worker, name='approve_worker'),
     path('approve_worker/<int:user_id>/', views.approve_worker, name='approve_worker'),
     path('provider_bookings/userpage.html', views.providerpage, name='providerpage'),
     path('bookinghistory/userpage.html', views.providerpage, name='providerpage'),
     path('bookinghistory/userpage', views.userpage, name='userpage'),
     path('bookinghistory/providerpage', views.providerpage, name='providerpage'),
     path('worker_requests', views.worker_requests, name='worker_requests'),
     path('worker_requests/<int:user_id>/', views.worker_requests, name='worker_requests'),
     path('providerpage/worker_requests/<int:user_id>/', views.approve_worker, name='approve_worker'),
     path('available_workers/<int:branchid_id>/<str:district>/', views.available_workers, name='available_workers'),
     path('available_workers/<int:branchid_id>/<str:district>/<int:booking_id>/providerpage/', views.available_workers, name='available_workers'),
     path('available_workers/<int:providerid_id>/<str:district>/<int:booking_id>/providerpage.html/', views.available_workers, name='available_workers_html'),
     path('assign_worker/', views.assign_worker, name='assign_worker'),
     path('workerjob/', views.worker_job, name='workerjob'),
     path('assignedwork/', views.assignedwork, name='assignedwork'),
     path('update_status/', views.update_status, name='update_status'),
     path('generate_report/<int:bookingid_id>/', views.render_report_form, name='render_report_form'),
     path('generate_report/', views.generate_report, name='generate_report'),
     path('provider/<int:userid>/workers/', views.worker_list, name='worker_list'),
     path('worker_report/<int:managerid>/', views.worker_report, name='worker_report'),
     path('client_bookings/<int:client_id>/', views.client_bookings, name='client_bookings'),
     path('assign_workers/<int:reportid>/', views.assign_workers, name='assign_workers'),
     path('assign_workers_service/', views.assign_workers_service, name='assign_workers_service'),
     path('client_work_reports/<int:client_id>/', views.client_work_reports, name='client_work_reports'),
     path('download_work_report/<int:report_id>/', views.download_worker_report, name='download_work_report'),
     path('client_work_reports/<int:client_id>/userpage', views.userpage, name='userpage'),
     path('assign_workers_service/assign_workers.html', views.providerpage, name='providerpage'),
     path('bookinghistory/providerpage', views.providerpage, name='providerpage'),
     path('bookinghistory/user_logout', views.user_logout, name='user_logout'),
     path('approve_report/', views.approve_report, name='approve_report'),
     path('cancel_service/', views.cancel_service, name='cancel_service'),
     path('update_rating/', views.update_rating, name='update_rating'),
     path('update_review/', views.update_review, name='update_review'),
     path('update-service-and-booking/<int:booking_id>/', views.update_service_and_booking, name='update_service_and_booking'),
     path('client_work_reports/<int:client_id>/payment_success', views.payment_success, name='payment_success'),
     path('payment_success/', payment_success, name='payment_success'),
     path('add_service/', add_service, name='add_service'),
     path('add_branch/', add_branch, name='add_branch'),
     path('add_branch_page/<int:provider_id>/', add_branch_page, name='add_branch_page'),
     path('branch_page/<int:provider_id>/', views.branch_page, name='branch_page'),
     path('branch_page/<int:provider_id>/providerpage', providerpagehome, name='providerpage'),
     path('manager_registration/<int:provider_id>/<int:branch_id>/', manager_registration, name='manager_registration'),
     path('managerpage/', managerpage, name='managerpage'),
     path('worker_requests/<int:user>/', worker_requests, name='worker_requests'),
     path('activate_worker/<int:user_id>/<int:manager_id>/<int:branch_id>/', activate_worker, name='activate_worker'),
     path('service/<int:category>/', service_providers_by_category, name='service_providers_by_category'),
     path('service/<int:category>/<int:userid>/', service_providers_by_category, name='service_providers_by_category'),
     path('service/<int:category>/<int:userid>/userpage', userpagehome, name='userpagehome'),
     path('service/<int:category>/<int:userid>/user_logout', userlogout, name='userlogout'),
     path('render_booking_form/<int:client_id>/<int:branchid>/', render_booking_form, name='render_booking_form'),
     path('provider_booking/<int:user>/', provider_bookings, name='provider_booking'),
     path('provider_booking/<int:user>/managerpage', managerpagehome, name='managerpagehome'),
     path('apply_leave/', apply_leave, name='apply_leave'),
     path('leave_success/', views.leave_success, name='leave_success'),
     path('leave_requests/<int:provider_id>/', leave_requests, name='leave_requests'),
     path('leave_requests/<int:provider_id>/providerpage', providerpagehome, name='providerpagehome'),
     path('approve_leave/<int:leave_id>/', approve_leave, name='approve_leave'),
     path('cancel_leave/<int:leave_id>/', cancel_leave, name='cancel_leave'),
     path('update_service_status/<int:report_id>/', update_service_status, name='update_service_status'),
     path('worker_report/<int:provider_id>/', views.worker_report, name='worker_report'),
     path('managerpage/<int:provider_id>/', providerpage , name='providerpage'),
     path('branch_list/<int:provider_id>/', branch_list, name='branch_list'),
     path('branch_list/<int:provider_id>/providerpage', providerpagehome, name='providerpagehome'),
     path('help_assistant/', help_assistant, name='help_assistant'),
     path('help_assistant/userpage', userpage, name='userpage'),
     path('help_assistant/user_logout', user_logout, name='user_logout'),


]
