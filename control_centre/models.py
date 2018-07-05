from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, Sum, Avg

User = settings.AUTH_USER_MODEL


class Owner(models.Model):
    user = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE, unique=True)
    design = models.ForeignKey(User, related_name='designer',blank=True, null=True, on_delete=models.CASCADE)
    purchase = models.ForeignKey(User, related_name='purchaser',blank=True, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(User, related_name='store_keeper',blank=True, null=True, on_delete=models.CASCADE)
    fabrication = models.ForeignKey(User, related_name='fabricator',blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_edit_url(self):
        return reverse("edit_owner", kwargs={"pk": self.pk})


class Project(models.Model):
    name = models.CharField(max_length=180)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class IsoManagerQueryset(models.query.QuerySet):
    def total_inch_dia(self):
        return self.aggregate(Sum('joint__inch_dia'))


class IsoManager(models.Manager):
    def get_queryset(self):
        return IsoManagerQueryset(self.model, using=self._db)


class Iso(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    iso_no = models.CharField(verbose_name='iso no/line no', max_length=200, blank=True, null=True, unique=True)
    no_of_joints = models.IntegerField(blank=True, null=True)
    inch_dia = models.IntegerField(verbose_name='Total Inch Dia', blank=True, null=True)

    objects = IsoManager()

    def __str__(self):
        return self.iso_no


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, unique=True)
    content = models.TextField()
    image = models.FileField(null=True, blank=True)
    published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
