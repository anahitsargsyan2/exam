from django.urls import path

from . import views

app_name = "courses"
urlpatterns = [
    path("", views.course_list, name="course_list"),
    path('<int:id>/', views.course_detail, name='course_detail'),
    path("register/", views.register, name= "register"),
    path("login/", views.login, name="login"),
    path("logout/", views.log_out, name="logout"),
]