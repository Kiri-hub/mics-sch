# Generated by Django 4.2.23 on 2025-06-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_rename_students_course_student_students_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='lesson_in_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='per_lesson',
            field=models.BooleanField(default=False),
        ),
    ]
