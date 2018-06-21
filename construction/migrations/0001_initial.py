# Generated by Django 2.0 on 2018-06-21 09:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Joint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joint_no', models.CharField(blank=True, max_length=50, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('sch', models.CharField(blank=True, max_length=50, null=True, verbose_name='Schedule')),
                ('welder', models.CharField(blank=True, max_length=80, null=True, verbose_name='Welder Name')),
                ('fabricator', models.CharField(blank=True, max_length=80, null=True, verbose_name='Fabricator Name')),
                ('supervisor', models.CharField(blank=True, max_length=80, null=True, verbose_name='Supervisor Name')),
                ('engineer', models.CharField(blank=True, max_length=80, null=True, verbose_name='Engineer Name')),
                ('hours_worked', models.IntegerField(blank=True, null=True, verbose_name='Hours consumed')),
                ('crew_members', models.IntegerField(blank=True, null=True, verbose_name='No.of Crew')),
                ('date_completed', models.DateField(default=django.utils.timezone.now)),
                ('inch_dia', models.IntegerField(blank=True, null=True)),
                ('actual_inch_dia', models.IntegerField(blank=True, null=True)),
                ('man_hours', models.FloatField(blank=True, null=True, verbose_name='Total Man Hours Taken')),
                ('ndt', models.CharField(choices=[('Not Started', 'Not Started'), ('Going on', 'Going on'), ('Completed', 'Completed')], default='Not Started', max_length=40, verbose_name='NDT Status')),
                ('hydro', models.CharField(choices=[('Not Started', 'Not Started'), ('Going on', 'Going on'), ('Completed', 'Completed')], default='Not Started', max_length=40, verbose_name='Hydrotest Status')),
                ('radio', models.CharField(choices=[('Not Started', 'Not Started'), ('Going on', 'Going on'), ('Completed', 'Completed')], default='Not Started', max_length=40, verbose_name='Radiography Status')),
                ('iso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.Iso')),
            ],
        ),
    ]
