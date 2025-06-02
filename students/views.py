from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Student
from .forms import StudentForm


def homepage(request):
    students = Student.objects.order_by("id")
    return render(request, 'students/base.html', {"students": students})


def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("homepage"))
    form = StudentForm()
    return render(request, 'students/create_student.html', {"form": form})


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
    return render(request, 'students/create_student.html', {"form": form})



def view_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/view_student.html', {"student": student})