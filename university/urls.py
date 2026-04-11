from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('student/search/', views.student_search, name='student_search'),
    path('courses/', views.course_list, name='course_list'),
    path('grade/add/', views.add_grade, name='add_grade'),
    path('debug/env/', views.debug_env, name='debug_env'),
]