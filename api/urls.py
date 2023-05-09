from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('admins/', views.getadminAPI),
    path('admins/<str:id>/', views.getAdmin),
    path('students/', views.getStudentsAPI),
    path('students/<str:id>', views.getUser),
    path('subjects/', views.getSubjectsAPI),
     path('subjects/<str:offerCode>', views.getSubjectsAPI),
    path('colleges/', views.getCollegesAPI),
    path('colleges/<str:id>', views.getCollegesAPI),
     path('enrollment/', views.enrollment_list),
    path('enrollment/<str:student_id>', views.enrollment_list),

    path('login/', views.loginAPI),
    ]