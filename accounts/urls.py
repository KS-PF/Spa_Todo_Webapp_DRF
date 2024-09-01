from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'accounts'
urlpatterns = [
    path('', views.UserDetailView.as_view(), name="user_detail"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]

urlpatterns = format_suffix_patterns(urlpatterns)