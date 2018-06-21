from django.db import models
from django.utils import timezone
from materials.models import Iso
from django.db.models.signals import pre_save
from hr.models import Welder, Fabricator, Engineer, Supervisor

NDT_CHOICES = (
                ('Not Started', 'Not Started'),
                ('Going on', 'Going on'),
                ('Completed', 'Completed'),
                  )
UNIT_CHOICES = (
                ('Nos', 'Nos'),
                ('Mtr', 'Mtr'),
                  )


class Joint(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    joint_no = models.CharField(max_length=50, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    sch = models.CharField(verbose_name='Schedule', max_length=50, blank=True, null=True)
    welder = models.ForeignKey(Welder, on_delete=models.CASCADE)
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE )
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
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