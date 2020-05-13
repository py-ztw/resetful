from django.db import models


# Create your models here.

class UserInfo(models.Model):
    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other")
    )

    username = models.CharField(max_length=80)
    password = models.CharField(max_length=64, blank=True, null=True)
    gender = models.SmallIntegerField(choices=gender_choices, default=1)

    class Meta:
        db_table = "ba_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Student(models.Model):
    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other")
    )

    studentname = models.CharField(max_length=80)
    password = models.CharField(max_length=64, blank=True, null=True)
    gender = models.SmallIntegerField(choices=gender_choices, default=1)

    class Meta:
        db_table = "ba_student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.studentname

class Employee(models.Model):
    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other")
    )
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64, blank=True, null=True)
    gender = models.SmallIntegerField(choices=gender_choices, default=1)
    phone = models.CharField(max_length=11, null=True, blank=True)
    pic = models.ImageField(upload_to="pic", default="pic/1.jpeg")

    class Meta:
        db_table = "bz_employee"
        verbose_name = "员工"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
