from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student, ChessCourse, Professor
from .forms import StudentForm, ProfessorForm


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
            'status': 'Active' if student.is_active == True else 'Not active'
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
    professors = Professor.get_all_professors()
    professors_dict = {}
    for professor in professors:
        total_income = professor.get_professor_total_income()
        professor_rate = professor.get_professor_total_rate()
        school_rate = professor.get_professor_total_school_rate()
        professor_students = professor.get_all_students()
        professors_dict[professor.pk] = {
            "name": professor.name,
            "surname": professor.surname,
            "total_income": total_income,
            "professor_rate": professor_rate,
            "school_rate": school_rate,
            "professor_students_num": len(professor_students),
        }
    context = {
        "professors": professors_dict,
        "total_income": Professor.get_all_professors_income(),
        "total_professors_rate": Professor.get_all_professors_rate(),
        "total_school_rate": Professor.get_total_school_rate(),
        "all_students": Student.len_all_students(),
    }
    return render(request, 'students/view_school_profit.html', context=context)


def view_professor(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    total_income = professor.get_professor_total_income()
    professor_rate = professor.get_professor_total_rate()
    school_rate = professor.get_professor_total_school_rate()
    professor_students = professor.get_all_students()
    professor_dict = {
        "name": professor.name,
        "surname": professor.surname,
        "total_income": total_income,
        "professor_rate": professor_rate,
        "professor_students": professor_students,
        "school_rate": school_rate,
        "professor_students_num": len(professor_students),
    }
    students = {}
    for student in professor_students:
        courses = student.students_courses.all()
        students[student.pk] = {
            'name': student.name,
            'surname': student.surname,
            'courses': courses,
            'professor': student.professor,
            'status': 'Active' if student.is_active == True else 'Not active',
            'total_income': sum(course.course_price for course in courses),
            'professor_rate': sum(course.professor_rate for course in courses),
            'school_rate': sum(course.get_school_rate() for course in courses),
        }
    return render(request, 'students/view_professor.html', {'students': students, 'professor': professor_dict})


def view_professors(request):
    professors_qs = Professor.objects.all()
    professors_dict = {}
    for professor in professors_qs:
        professors_dict[professor.pk] = {
            'name': professor.name,
            'surname': professor.surname,
        }
    return render(request, 'students/view_professors.html', {"professors": professors_dict})


def create_professor(request):
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('homepage'))
    form = ProfessorForm()
    return render(request, 'students/professor_form.html', {'form': form})

