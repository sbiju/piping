from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from django.shortcuts import HttpResponse
from django.db.models import Q
User = settings.AUTH_USER_MODEL

RED_CHOICES = (
                ('CONCENTRIC', 'CONCENTRIC'),
                ('ECCENTRIC', 'ECCENTRIC'),
                  )

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


class BoltSize(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)


    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']
        
        
class Size(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True, null=True)


    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class Service(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class Unit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']
        

class Material(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class Schedule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class LineClass(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class FlangeClass(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class GasketMaterial(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class BoltGrade(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class SpoolStatus(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']


class Pefs(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FitUpStatus(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WeldStatus(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MaterialGrade(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        

class ValveType(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        
        
class ValveEnd(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class IsoManagerQueryset(models.query.QuerySet):

    def by_range(self, start_date, end_date):
        if end_date is None:
            return self.filter(date_completed__gte=start_date)
        return self.filter(date_completed__gte=start_date).filter(date_completed__lte=end_date)

class IsoManager(models.Manager):
    def get_queryset(self):
        return IsoManagerQueryset(self.model, using=self._db)

    # def get_queryset(self):
    #     return self.get_queryset(is_approved=True)

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
    iso_no = models.CharField(verbose_name='iso no/line no', max_length=200, \
    unique=True, blank=True, null=True)
    pefs = models.ForeignKey(Pefs, on_delete=models.CASCADE, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    line_class = models.ForeignKey(LineClass, on_delete=models.CASCADE, blank=True, null=True)
    is_approved = models.BooleanField(default=True)

    objects = IsoManager()

    def __str__(self):
        return self.iso_no

    def get_absolute_url(self):
        return reverse("iso_detail", kwargs={"pk": self.pk})
        
    def get_edit_url(self):
        return reverse("iso_edit", kwargs={"pk": self.pk})    

    class Meta:
        ordering = ['service__name']


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


class Valve(models.Model):
    type = models.ForeignKey(ValveType, on_delete=models.CASCADE, blank=True, null=True)
    end_type = models.ForeignKey(ValveEnd, on_delete=models.CASCADE, blank=True, null=True)
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)

    def __str__(self):
        return self.type


class Elbow(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(MaterialGrade, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)
    
    def __str__(self):
        return self.size.name


class Tee(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(MaterialGrade, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)
    
    def __str__(self):
        return self.size.name
        
        
class Coupling(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(MaterialGrade, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)
    
    def __str__(self):
        return self.size.name
        
        
class Reducer(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(MaterialGrade, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=30, choices=RED_CHOICES, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)
    
    def __str__(self):
        return self.size.name
        
        
class BranchFitting(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(MaterialGrade, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(verbose_name='Quantity in Nos', blank=True, null=True)
    
    def __str__(self):
        return self.size.name        


class Bolt(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.ForeignKey(BoltGrade, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(BoltSize, on_delete=models.CASCADE, blank=True, null=True)
    length = models.CharField(max_length=50, blank=True, null=True)
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

    def erected(self):
        return self.filter(spool_status__name='erected')


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
        
    class Meta:
        unique_together = ('iso', 'spool_tag')
        ordering = ['-timestamp']
    




