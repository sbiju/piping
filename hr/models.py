from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

NDT_CHOICES = (
                ('Not Started', 'Not Started'),
                ('Going on', 'Going on'),
                ('Completed', 'Completed'),
                  )


class Owner(models.Model):
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    design = models.ForeignKey(User, related_name='designer',blank=True, null=True, on_delete=models.CASCADE)
    purchase = models.ForeignKey(User, related_name='purchaser',blank=True, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(User, related_name='store_keeper',blank=True, null=True, on_delete=models.CASCADE)
    fabrication = models.ForeignKey(User, related_name='fabricator',blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def post_save_user_model_reciever(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Owner.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_reciever, sender=User)


class Project(models.Model):
    name = models.CharField(max_length=180)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Iso(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    iso_no = models.CharField(verbose_name='iso no/line no', max_length=200, blank=True, null=True)
    no_of_joints = models.IntegerField(blank=True, null=True)
    inch_dia = models.IntegerField(verbose_name='Total Inch Dia', blank=True, null=True)

    def __str__(self):
        return self.iso_no


class Employee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=180, blank=True, null=True)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    emplyee_no = models.CharField(max_length=180, blank=True, null=True, unique=True)
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.first_name


class Welder(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name


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

