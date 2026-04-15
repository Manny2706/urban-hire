from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserLogoutView, UserSignupView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='customer-signup'),
    path('login/', TokenObtainPairView.as_view(), name='customer-login'),
    path('logout/', UserLogoutView.as_view(), name='customer-logout'),
]
