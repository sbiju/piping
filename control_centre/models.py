from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from django.shortcuts import HttpResponse
from django.db.models import Q
User = settings.AUTH_USER_MODEL


class Owner(models.Model):
    user = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE, unique=True)
    design = models.ForeignKey(User, related_name='designer',blank=True, null=True, on_delete=models.CASCADE)
    purchase = models.ForeignKey(User, related_name='purchaser',blank=True, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(User, related_name='store_keeper',blank=True, null=True, on_delete=models.CASCADE)
    fabrication = models.ForeignKey(User, related_name='fabricator',blank=True, null=True, on_delete=models.CASCADE)
    const_head = models.ForeignKey(User, related_name='construction_head',blank=True, null=True, on_delete=models.CASCADE)
    qc = models.ForeignKey(User, related_name='qc',blank=True, null=True, on_delete=models.CASCADE)
    hr = models.ForeignKey(User, related_name='hr',blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_edit_url(self):
        return reverse("edit_owner", kwargs={"pk": self.pk})


class Project(models.Model):
    name = models.CharField(max_length=180)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# class IsoManagerQueryset(models.query.QuerySet):
#
#     def total_inch_dia(self):
#         return self.aggregate(Sum('joint__inch_dia'))


class Size(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Service(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class LineClass(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class FlangeClass(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class GasketMaterial(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class BoltGrade(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class SpoolStatus(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name


class FabStatus(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class FitUpStatus(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class WeldStatus(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class IsoManager(models.Manager):
    # def get_queryset(self):
    #     return IsoManagerQueryset(self.model, using=self._db)

    def get_queryset(self):
        return super().get_queryset().filter(is_approved=True)

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(iso_no__icontains=query) |
                         Q(service__name__icontains=query) |
                         Q(line_class__name__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs


class Iso(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    iso_no = models.CharField(verbose_name='iso no/line no', max_length=200, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    line_class = models.ForeignKey(LineClass, on_delete=models.CASCADE, blank=True, null=True)
    is_approved = models.BooleanField(default=True)

    objects = IsoManager()

    def __str__(self):
        return self.iso_no

    def get_absolute_url(self):
        return reverse("iso_detail", kwargs={"pk": self.pk})


class Pipe(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,  blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True)
    length = models.IntegerField(verbose_name='Length in Meter', blank=True, null=True)

    def __str__(self):
        return str(self.size)

    def get_edit_url(self):
        return reverse("edit_pipe", kwargs={"pk": self.pk})


class Flange(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    flange_class = models.ForeignKey(FlangeClass, on_delete=models.CASCADE, blank=True, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)

    def __str__(self):
        return self.size.name


class Fitting(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)

    def __str__(self):
        return self.name


class Bolt(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(BoltGrade, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    length = models.ForeignKey(Size, related_name='bolt_length', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)

    def __str__(self):
        return self.size.name


class Gasket(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    gasket_material = models.ForeignKey(GasketMaterial, on_delete=models.CASCADE, blank=True, null=True)
    gasket_class = models.ForeignKey(FlangeClass, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)

    def __str__(self):
        return self.size.name


class SpoolManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(spool_tag__icontains=query)|
                         Q(timestamp__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs


class Spool(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    spool_tag = models.CharField(max_length=120, blank=True, null=True)
    spool_status = models.ForeignKey(SpoolStatus, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateField(blank=True, null=True)

    objects = SpoolManager()

    def __str__(self):
        return self.spool_tag

    def get_edit_url(self):
        return reverse("edit_spool", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("spool_detail", kwargs={"pk": self.pk})


class Fabrication(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    joint_no = models.CharField(verbose_name='Joint Nos', max_length=120, blank=True, null=True)
    fitup_status = models.ForeignKey(FitUpStatus, on_delete=models.CASCADE, blank=True, null=True)
    weld_status = models.ForeignKey(WeldStatus, on_delete=models.CASCADE, blank=True, null=True)
    fab_status = models.ForeignKey(FabStatus, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.iso.iso_no


