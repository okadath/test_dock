from django.conf.urls import url
from django.urls import path, include
from user_account import views

urlpatterns = [
    # path('',views.home,name='home'), 
    path('login_mail/',views.register_user,name='register_user'),
    path('',views.login_mail,name='login_mail'),
    # path('login_code/',views.login_code,name='login_code'),
    path('logout/',views.logout_view,name='logout'), 
    path('dashboard/',views.dashboard,name='dashboard'), 
]
