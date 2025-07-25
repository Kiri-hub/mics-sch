from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="professors_pics/", null=True)

    @classmethod
    def get_all_professors(cls):
        professors = Professor.objects.all()
        return professors

    @classmethod
    def get_all_professors_income(cls):
        professors = Professor.get_all_professors()
        all_professors_rate = 0
        for professor in professors:
            for course in professor.get_all_active_students_courses():
                if course.per_lesson:
                    all_professors_rate += course.course_price * course.lessons_in_month
                else:
                    all_professors_rate += course.course_price
        return all_professors_rate

    @classmethod
    def get_all_professors_rate(cls):
        professors = Professor.get_all_professors()
        all_professors_rate = 0
        for professor in professors:
            for course in professor.get_all_active_students_courses():
                if course.per_lesson:
                    all_professors_rate += course.professor_rate * course.lessons_in_month
                else:
                    all_professors_rate += course.professor_rate
        return all_professors_rate

    @classmethod
    def get_total_school_rate(cls):
        professors = Professor.get_all_professors()
        all_professors_rate = 0
        for professor in professors:
            for course in professor.get_all_active_students_courses():
                if course.per_lesson:
                    all_professors_rate += course.get_school_rate() * course.lessons_in_month
                else:
                    all_professors_rate += course.get_school_rate()
        return all_professors_rate

    def get_all_students(self):
        students = self.professor_students.all()
        return students

    def get_all_active_students(self):
        students = self.professor_students.filter(is_active=True)
        return students

    def get_all_active_students_courses(self):
        students = self.get_all_active_students()
        courses = []
        for student in students:
            courses.extend(student.students_courses.all())
        return courses

    def get_professor_total_income(self):
        courses = self.get_all_active_students_courses()
        total_income = sum(
            course.course_price * course.lessons_in_month if course.per_lesson
            else course.course_price for course in courses)
        return total_income

    def get_professor_total_rate(self):
        courses = self.get_all_active_students_courses()
        total_professors_rate = sum(
            course.professor_rate * course.lessons_in_month if course.per_lesson
            else course.professor_rate for course in courses)
        return total_professors_rate

    def get_professor_total_school_rate(self):
        total_income = self.get_professor_total_income()
        total_professors_rate = self.get_professor_total_rate()
        return total_income - total_professors_rate

    def __str__(self):
        return f"{self.name} {self.surname}"


class ChessCourse(models.Model):
    course_name = models.CharField(max_length=50)
    course_price = models.IntegerField()
    professor_rate = models.IntegerField()
    per_lesson = models.BooleanField(default=False)
    lessons_in_month = models.IntegerField(null=True, blank=True)

    def get_school_rate(self):
        return self.course_price - self.professor_rate

    def __str__(self):
        return f"{self.course_name}"


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, related_name="professor_students")
    students_courses = models.ManyToManyField(ChessCourse, related_name="course_students")
    notations = models.TextField(max_length=1000, default="Поки-що немає нотатків")


    @classmethod
    def get_all_students(cls):
        students = Student.objects.all()
        return students

    def get_total_income_from_student(self):
        total_income_from_student = 0
        for course in self.students_courses.all():
            if course.per_lesson:
                total_income_from_student += course.course_price * course.lessons_in_month
            else:
                total_income_from_student += course.course_price
        return total_income_from_student

    def get_total_school_rate_from_student(self):
        total_school_rate_from_student = 0
        for course in self.students_courses.all():
            if course.per_lesson:
                total_school_rate_from_student = course.get_school_rate() * course.lessons_in_month
            else:
                total_school_rate_from_student = course.course_price - course.professor_rate
        return total_school_rate_from_student


    def get_total_professore_rate_from_student(self):
        total_professore_rate_from_student = 0
        for course in self.students_courses.all():
            if course.per_lesson:
                total_professore_rate_from_student += course.professor_rate * course.lessons_in_month
            else:
                total_professore_rate_from_student += course.professor_rate
        return total_professore_rate_from_student


    @classmethod
    def get_all_active_students(cls):
        students = Student.objects.filter(is_active=True)
        return students

    @classmethod
    def len_all_students(cls):
        students = Student.get_all_students()
        students_amount = len(students)
        return students_amount

    def __str__(self):
        return f"{self.name} {self.surname}"
