from django.urls import path
from .views import LoginView, SignUpView, logout_view


app_name = 'core'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('logout/', logout_view, name='logout'),
]