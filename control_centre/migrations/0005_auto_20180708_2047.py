# Generated by Django 2.0 on 2018-07-08 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0004_auto_20180708_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iso',
            name='material_name',
        ),
        migrations.RemoveField(
            model_name='iso',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='iso',
            name='size',
        ),
        migrations.RemoveField(
            model_name='iso',
            name='unit',
        ),
    ]