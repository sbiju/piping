# Generated by Django 2.0 on 2018-02-18 17:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculations', '0007_auto_20180216_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialdata',
            name='purchaser',
            field=models.ManyToManyField(related_name='purchase_staff', to=settings.AUTH_USER_MODEL),
        ),
    ]
