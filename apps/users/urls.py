from django.urls import path

from .views import UserLogoutView, UserSignupView, UserLoginView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='customer-signup'),
    path('login/', UserLoginView.as_view(), name='customer-login'),
    path('logout/', UserLogoutView.as_view(), name='customer-logout'),
]
