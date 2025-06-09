from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.surname}"


class ChessCourse(models.Model):
    course_name = models.CharField(max_length=50)
    course_price = models.IntegerField()
    professor_rate = models.IntegerField()

    def __str__(self):
        return f"{self.course_name}"



class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, related_name="professor_students")
    students_course = models.ManyToManyField(ChessCourse, related_name="course_students")

    def __str__(self):
        return f"{self.name} {self.surname}"
