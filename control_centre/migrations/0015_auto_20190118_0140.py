# Generated by Django 2.0 on 2019-01-17 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0014_auto_20190118_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bolt',
            name='length',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
