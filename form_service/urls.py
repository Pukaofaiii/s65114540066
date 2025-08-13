from django.urls import path

from form_service import views 

urlpatterns = [
    path("service",views.service_user , name="service"),
    path("table_list",views.table_list , name="table_list"),
    path("edit_service/<int:id>",views.edit_service ,name="edit_service"),
    path("table_list/detail/<int:id>",views.detail,name="detail"),
    
]