from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student, ChessCourse, Professor
from .forms import StudentForm


def homepage(request):
    students_qs = Student.objects.order_by("id")
    students_dict = {}
    for student in students_qs:
        courses = student.students_courses.all()
        students_dict[student.pk] = {
            'name': student.name,
            'surname': student.surname,
            'courses': courses,
            'professor': student.professor,
        }
    return render(request, 'students/homepage.html', {'students': students_dict})


def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("homepage"))
    form = StudentForm()
    return render(request, 'students/student_form.html', {"form": form, "action": "Create"})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect(reverse("homepage"))


def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect(reverse("homepage"))
    form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {"form": form, "action": "Update"})



def view_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/view_student.html', {"student": student})


def view_school_profit(request):
    all_students = Student.objects.all()
    school_profit = sum(course.course_price for student in all_students for course in student.students_courses.all())
    return render(request, 'students/view_school_profit.html', {"school_profit": school_profit})


def view_professor_profit(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    students = professor.professor_students.all()
    professor_profit = sum(course.course_price for student in students for course in student.students_course.all())
    return render(request, 'students/view_professor_profit.html', {"professor_profit": professor_profit})
