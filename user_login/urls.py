from django.urls import path , include
from user_login import views


urlpatterns = [
    path("login/",views.login , name="login"),
    path('logout',views.user_logout, name='logout'),
    path('register/',views.user_register, name='register'),
]