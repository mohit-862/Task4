from django.urls import path
from .views import index,user_login,user_register,user_verify,dashboard,logout


urlpatterns = [
    path('',index,name = 'index'),
    path('user-login',user_login,name="user_login"),
    path('user-register',user_register,name="user_register"),
    path('user-verify',user_verify,name="user_verify"),
    path('dashboard',dashboard,name="dashboard"),
    path('logout',logout,name="logout")
]
