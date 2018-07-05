from django.db import models
from django.utils import timezone
from materials.models import Iso
from django.db.models.signals import pre_save
from django.db.models import Sum
from hr.models import Employee

NDT_CHOICES = (
                ('Not Started', 'Not Started'),
                ('Going on', 'Going on'),
                ('Completed', 'Completed'),
                  )
UNIT_CHOICES = (
                ('Nos', 'Nos'),
                ('Mtr', 'Mtr'),
                  )

STATUS_CHOICES = (
                ('Passed', 'Passed'),
                ('Failed', 'Failed'),
                ('Pending', 'Pending'),
                  )


class JointManagerQueryset(models.query.QuerySet):

    def by_range(self, start_date, end_date):
        if end_date is None:
            return self.filter(date_completed__gte=start_date)
        return self.filter(date_completed__gte=start_date).filter(date_completed__lte=end_date)

    def total_inch_dia(self):
        return self.aggregate(Sum('inch_dia'))

    def recent(self):
        return self.order_by('-date_completed')

    def passed(self):
        return self.recent().status('Passed')

    def failed(self):
        return self.recent().status('Failed')



class JointManager(models.Manager):
    def get_queryset(self):
        return JointManagerQueryset(self.model, using=self._db)


class Joint(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    joint_no = models.CharField(max_length=50, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    sch = models.CharField(verbose_name='Schedule', max_length=50, blank=True, null=True)
    welder = models.ForeignKey(Employee, related_name='welder', on_delete=models.CASCADE)
    fabricator = models.ForeignKey(Employee, related_name='fabricator',  on_delete=models.CASCADE )
    supervisor = models.ForeignKey(Employee, related_name='supervisor', on_delete=models.CASCADE)
    engineer = models.ForeignKey(Employee, related_name='engineer', on_delete=models.CASCADE)
    hours_worked = models.IntegerField(verbose_name='Hours consumed', blank=True, null=True)
    crew_members = models.IntegerField(verbose_name='No.of Crew', blank=True, null=True)
    date_completed = models.DateField(default=timezone.now)
    inch_dia = models.IntegerField(blank=True, null=True)
    actual_inch_dia = models.IntegerField(blank=True, null=True)
    man_hours = models.FloatField(verbose_name='Total Man Hours Taken', blank=True, null=True)
    ndt = models.CharField(verbose_name='NDT Status', max_length=40, choices=NDT_CHOICES,
                           default='Not Started')
    hydro = models.CharField(verbose_name='Hydrotest Status', max_length=40, choices=NDT_CHOICES,
                             default='Not Started')
    radio = models.CharField(verbose_name='Radiography Status', max_length=40, choices=NDT_CHOICES,
                             default='Not Started')
    status = models.CharField(verbose_name='Joint Status', max_length=40, choices=STATUS_CHOICES,
                             default='Pending')
    qc_checked = models.DateField(blank=True, null=True)

    objects = JointManager()

    def __str__(self):
        return self.joint_no


def total_inch_receiver(sender, instance, *args, **kwargs):
    size = instance.size
    inch_dia = size
    instance.inch_dia = inch_dia
    crew_members = instance.crew_members
    hours_worked = instance.hours_worked

    sch = instance.sch
    if sch == '60':
        actual_inch_dia = size * 1.5
    elif sch == '80':
        actual_inch_dia = size * 2
    elif sch == '120':
        actual_inch_dia = size * 3
    elif sch == '160':
        actual_inch_dia = size * 4
    else:
        actual_inch_dia = size
    instance.actual_inch_dia = actual_inch_dia

    try:
        man_hours =  (crew_members * hours_worked) / actual_inch_dia
    except:
        man_hours = 0
    instance.man_hours = man_hours

pre_save.connect(total_inch_receiver, sender=Joint)