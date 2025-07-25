from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage, name="homepage"),
    path('view-student/<int:pk>/', views.view_student, name="view_student"),
    path('delete-student/<int:pk>/', views.delete_student, name="delete_student"),
    path('create-student/', views.create_student, name="create_student"),
    path('update-student/<int:pk>/', views.update_student, name="update_student"),
    path('view-school-profit/', views.view_school_profit, name="view_school_profit"),
    path('view-professor/<int:pk>/', views.view_professor, name="view_professor"),
    path('view-professors/', views.view_professors, name="view_professors"),
    path('create-professor/', views.create_professor, name="create_professor"),
]