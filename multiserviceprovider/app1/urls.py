from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', register, name="signup"),
    path('userpage/',userpage, name='userpage'),
    path('signin/signup', register ),
    path('signin/index', index ),
    path('signup/signin', signin ),
    path('signup/index', index ),
    path('signin/signin', signin ),
    
]