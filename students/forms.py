from django.forms import ModelForm
from .models import Student, Professor


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["name", "surname", "is_active", "professor", "students_courses", "notations"]


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ["name", "surname", "picture"]