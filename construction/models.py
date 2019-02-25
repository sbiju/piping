from django.db import models
from django.utils import timezone
from control_centre.models import Iso
from django.db.models.signals import pre_save
from django.db.models import Sum
from hr.models import Employee
from control_centre.models import Size, Schedule, FitUpStatus, WeldStatus
from django.urls import reverse


class NdtStatus(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class JointManagerQueryset(models.query.QuerySet):

    def by_range(self, start_date, end_date):
        if end_date is None:
            return self.filter(date_completed__gte=start_date)
        return self.filter(date_completed__gte=start_date).filter(date_completed__lte=end_date)

    def total_inch_dia(self):
        return self.aggregate(Sum('inch_dia'))


class JointManager(models.Manager):
    def get_queryset(self):
        return JointManagerQueryset(self.model, using=self._db)

    def recent(self):
        return self.get_queryset().order_by('-date_completed')

    def fitup_done(self):
        return self.recent().filter(fitup_status__name='fitup_completed')

    def welded(self):
        return self.recent().filter(weld_status__name='welded')


class Joint(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    joint_no = models.CharField(max_length=50, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    sch = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True)
    welder = models.ForeignKey(Employee, related_name='welder', on_delete=models.CASCADE)
    fabricator = models.ForeignKey(Employee, related_name='fabricator',  on_delete=models.CASCADE )
    supervisor = models.ForeignKey(Employee, related_name='supervisor', on_delete=models.CASCADE)
    engineer = models.ForeignKey(Employee, related_name='engineer', on_delete=models.CASCADE)
    hours_worked = models.IntegerField(verbose_name='Hours consumed', blank=True, null=True)
    crew_members = models.IntegerField(verbose_name='No.of Crew', blank=True, null=True)
    date_completed = models.DateField(verbose_name='Date', default=timezone.now)
    inch_dia = models.IntegerField(blank=True, null=True)
    actual_inch_dia = models.IntegerField(blank=True, null=True)
    man_hours = models.FloatField(verbose_name='Total Man Hours Taken', blank=True, null=True)
    fitup_status = models.ForeignKey(FitUpStatus, on_delete=models.CASCADE, blank=True, null=True)
    weld_status = models.ForeignKey(WeldStatus, on_delete=models.CASCADE, blank=True, null=True)
    iso_comleted = models.BooleanField(verbose_name='Is Mechanical Job Completed for this ISO', default=False)

    objects = JointManager()

    def __str__(self):
        return str(self.joint_no)

    class Meta:
        ordering = ['-date_completed']
        unique_together = ['iso', 'joint_no']


    @property
    def pipe_size(self):
        return int(self.size.name)

    @property
    def pipe_sch(self):
        return int(self.sch.name)


class QcManager(models.Manager):

    def fitup_passed(self):
        return self.filter(fitup_status__name='passed')

    def fitup_failed(self):
        return self.filter(fitup_status__name='failed')

    def welding_passed(self):
        return self.filter(welding_status__name='passed')

    def welding_failed(self):
        return self.filter(welding_status__name='failed')

    def radiography_passed(self):
        return self.filter(radiography_status__name='passed')

    def radiography_failed(self):
        return self.filter(radiography_status__name='failed')

    def hydro_passed(self):
        return self.filter(hydro_test_status__name='passed')


class Qc(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    joint = models.ForeignKey(Joint, on_delete=models.CASCADE)
    fitup_status = models.ForeignKey(NdtStatus, related_name='fitup_status', on_delete=models.CASCADE, default= 1)
    fitup_inspection_date = models.DateField(default=timezone.now, blank=True, null=True)
    welding_status = models.ForeignKey(NdtStatus, related_name='welding_status', on_delete=models.CASCADE, blank=True, null=True)
    welding_inspection_date = models.DateField(blank=True, null=True)
    hydro_test_status = models.ForeignKey(NdtStatus, related_name='hydro_status', on_delete=models.CASCADE, blank=True, null=True)
    hydro_test_inspection_date = models.DateField(blank=True, null=True)
    radiography_status = models.ForeignKey(NdtStatus, related_name='radio_status', on_delete=models.CASCADE, blank=True, null=True)
    radiography_inspection_date = models.DateField(blank=True, null=True)

    objects = QcManager()

    def __str__(self):
        return self.joint.joint_no

    def get_radio_url(self):
        return reverse("qc_radio_update", kwargs={"pk": self.pk})

    def get_fitup_url(self):
        return reverse("qc_fitup_update", kwargs={"pk": self.pk})

    def get_weld_url(self):
        return reverse("qc_weld_update", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-fitup_inspection_date']
        unique_together = ['iso', 'joint']


def total_inch_receiver(sender, instance, *args, **kwargs):
    pipe_size = instance.pipe_size
    pipe_sch = instance.pipe_sch
    crew_members = instance.crew_members
    hours_worked = instance.hours_worked
    if pipe_sch == 60:
        actual_inch_dia = pipe_size * 1.5
    elif pipe_sch == 80:
        actual_inch_dia = pipe_size * 2
    elif pipe_sch == 120:
        actual_inch_dia = pipe_size * 3
    elif pipe_sch == 160:
        actual_inch_dia = pipe_size * 4
    else:
        actual_inch_dia = pipe_size
    instance.actual_inch_dia = actual_inch_dia

    try:
        inch_dia = pipe_size
    except:
        inch_dia = 0
    instance.inch_dia = inch_dia

    try:
        man_hours =  (crew_members * hours_worked) / actual_inch_dia
    except:
        man_hours = 0
    instance.man_hours = man_hours

pre_save.connect(total_inch_receiver, sender=Joint)