# Create your models here.
from django.db import models

GRADES_CHOICES = (
    (float(1), float(1)),
    (float(1.5), float(1.5)),
    (float(2), float(2)),
    (float(2.5), float(2.5)),
    (float(3), float(3)),
    (float(3.5), float(3.5)),
    (float(4), float(4)),
    (float(4.5), float(4.5)),
    (float(5), float(5)),
    (float(5.5), float(5.5)),
    (float(6), float(6)),
)

class SchoolAdress(models.Model):
    street = models.CharField(max_length=100)
    building_number = models.IntegerField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100)

    def __str__(self):
        return self.lesson_name

    # class Meta: # aby tworzyć własne uprawnienia do panelu administracyjnego
    #     permissions = [
    #         ("can_create_lesson", "Can create lesson"),
    #         ("can_view_lesson", "Can view lesson"),
    #         ("can_update_lesson", "Can update lesson"),
    #         ("can_delete_lesson", "Can delete lesson"),
    #     ]
    #  default_permissions = ()  # tak można wyłączyć automatyczne CRUD

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Lesson)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# class TeacherLesson(models.Model):
#     teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
#     lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    
#     class Meta:
#         unique_together = ("teacher", "lesson")  # żeby istniała unikalność połączeń teacher i lesson

#     def __str__(self):
#         return f"{self.lesson.lesson_name} - {self.teacher.first_name} {self.teacher.last_name}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Lesson)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TeacherLessonStudent(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("teacher", "lesson", "student")  # żeby istniała unikalność połączeń teacher i lesson i student

    def __str__(self):
        return f"{self.lesson.lesson_name} | {self.teacher.first_name} {self.teacher.last_name} | {self.student.first_name} {self.student.last_name}"


class Grade(models.Model):
    teacher_lesson_student = models.ForeignKey(TeacherLessonStudent, on_delete=models.CASCADE)
    grade = models.FloatField(choices=GRADES_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.grade} - {self.teacher_lesson_student}"


class School(models.Model):
    name = models.CharField(max_length=300)
    address = models.OneToOneField(SchoolAdress, on_delete=models.SET_NULL, null=True)
    director = models.OneToOneField(Director, on_delete=models.SET_NULL, null=True)
    teachers = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True) # zastanów się czy to jest tu faktycznie potrzebne? chyba tylko w sytuacji wyświetlania danych szkoły





