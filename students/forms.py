from django.forms import ModelForm
from .models import Student


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["name", "surname", "is_active", "professor", "students_course"]