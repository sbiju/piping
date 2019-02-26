from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from control_centre.models import Project

DAY_CHOICES = (
                ('Present', 'Present'),
                ('Absent', 'Absent'),
                ('Vacation', 'On Vacation'),
                  )


class Designation(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class EmployeeManager(models.Manager):
    def recent(self):
        return self.order_by('designation', '-joined_date')

    def welders(self):
        return self.filter(designation__title='welder')

    def fabricators(self):
        return self.filter(designation__title='fabricator')

    def supervisors(self):
        return self.filter(designation__title='supervisor')

    def engineers(self):
        return self.filter(designation__title='engineer')


class Employee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    emplyee_no = models.CharField(max_length=180, blank=True, null=True, unique=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    joined_date = models.DateField(default=timezone.now)

    objects = EmployeeManager()

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return str(self.first_name)


class RosterManager(models.Manager):
    def absent_emp(self):
        return self.filter(absent=True)


class DailyReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    absent = models.BooleanField(default=False)
    timestamp = models.DateField(default=timezone.now)

    objects = RosterManager()

    def __str__(self):
        return self.employee.first_name

    class Meta:
        unique_together = ('employee', 'timestamp')
        ordering = ['-timestamp']

