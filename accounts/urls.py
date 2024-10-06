from django.urls import path
from accounts.views import *

urlpatterns = [
    path('signup/',SignupUser.as_view(),name='signup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='profile'),
]
