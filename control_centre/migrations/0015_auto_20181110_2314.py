# Generated by Django 2.0 on 2018-11-10 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0014_auto_20181110_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iso',
            name='iso_no',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='iso no/line no'),
        ),
    ]