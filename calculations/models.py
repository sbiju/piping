from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save

User = settings.AUTH_USER_MODEL


class Iso(models.Model):
    iso_no = models.CharField(verbose_name='iso no/line no', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.iso_no


class Owner(models.Model):
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    design = models.ForeignKey(User, related_name='designer',blank=True, null=True, on_delete=models.CASCADE)
    purchase = models.ForeignKey(User, related_name='purchaser',blank=True, null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(User, related_name='store_keeper',blank=True, null=True, on_delete=models.CASCADE)
    fabrication = models.ForeignKey(User, related_name='fabricator',blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class MaterialData(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    purchased = models.BooleanField(default=False)
    fabricated = models.BooleanField(default=False)
    issued = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=25, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse("update", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


def total_reciever(sender, instance, *args, **kwargs):
    quantity = instance.quantity
    price = instance.price
    try:
        total_price = quantity * price
    except:
        total_price = 0
        return total_price
    instance.total_price = total_price

pre_save.connect(total_reciever, sender=MaterialData)