from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils import timezone
from control_centre.models import Iso

UNIT_CHOICES = (
                ('Nos', 'Nos'),
                ('Mtr', 'Mtr'),
                  )


class MaterialData(models.Model):
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200,blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="Nos")
    quantity_purchased = models.IntegerField(blank=True, null=True)
    balance_purchase = models.IntegerField(verbose_name='Balance to be Purchased',blank=True, null=True)
    quantity_issued = models.IntegerField(blank=True, null=True)
    balance_issue = models.IntegerField(verbose_name='Balance to be Issued',blank=True, null=True)
    quantity_used = models.IntegerField(blank=True, null=True)
    balance_used = models.IntegerField(verbose_name='Balance to be Used', blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    purchased = models.BooleanField(default=False)
    fabricated = models.BooleanField(default=False)
    issued = models.BooleanField(default=False)
    date_entered = models.DateField(default=timezone.now)
    date_purchased = models.DateField(default=timezone.now)
    date_issued = models.DateField(default=timezone.now)
    date_fabricated = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(verbose_name='Price Paid', max_digits=25, decimal_places=2,
                                      blank=True, null=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse("update", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

    class Meta:
        unique_together = ('iso', 'name', 'size',)


def total_receiver(sender, instance, *args, **kwargs):
    quantity = instance.quantity
    price = instance.price
    quantity_purchased = instance.quantity_purchased
    quantity_issued = instance.quantity_issued
    try:
        stock = quantity - quantity_issued
    except:
        stock = 0
    instance.stock = stock
    try:
        balance_purchase = quantity - quantity_purchased
    except:
        balance_purchase = 0
    instance.balance_purchase = balance_purchase
    quantity_used = instance.quantity_used
    try:
        balance_used = quantity_issued - quantity_used
    except:
        balance_used = 0
    instance.balance_used = balance_used
    try:
        total_price = quantity_purchased * price
    except:
        total_price = 0
        return total_price
    instance.total_price = total_price

pre_save.connect(total_receiver, sender=MaterialData)


