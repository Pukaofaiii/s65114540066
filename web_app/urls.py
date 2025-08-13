from django.urls import path 
from web_app import views
from .views import *

urlpatterns = [
    path("",views.index , name="home"),
    path("contact",views.contact , name="contact"),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('update_profile_image/', update_profile_image, name='update_profile_image'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('service_rates', views.service_rates, name='service_rates'),
]