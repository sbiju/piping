from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from control_centre.models import Project
User = settings.AUTH_USER_MODEL


class Employee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    emplyee_no = models.CharField(max_length=180, blank=True, null=True, unique=True)
    designation = models.CharField(max_length=120, blank=True, null=True)
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.first_name)


class Welder(models.Model):
    welder_no = models.CharField(max_length=120, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee)


class Fabricator(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name


class Supervisor(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name


class Engineer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name

