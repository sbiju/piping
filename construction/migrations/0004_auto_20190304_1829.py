# Generated by Django 2.0 on 2019-03-04 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0003_auto_20190304_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joint',
            name='fitup_status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='control_centre.FitUpStatus'),
        ),
    ]
