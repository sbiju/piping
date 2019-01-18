# Generated by Django 2.0 on 2019-01-18 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0016_auto_20190118_1221'),
        ('construction', '0006_auto_20190118_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joint',
            name='status',
        ),
        migrations.AddField(
            model_name='joint',
            name='erection_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.FabStatus'),
        ),
        migrations.AddField(
            model_name='joint',
            name='fitup_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.FitUpStatus'),
        ),
        migrations.AddField(
            model_name='joint',
            name='weld_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.WeldStatus'),
        ),
    ]
