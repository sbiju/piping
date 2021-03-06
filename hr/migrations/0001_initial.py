# Generated by Django 2.0 on 2018-12-01 15:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('control_centre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=180)),
                ('last_name', models.CharField(blank=True, max_length=180, null=True)),
                ('emplyee_no', models.CharField(blank=True, max_length=180, null=True, unique=True)),
                ('joined_date', models.DateField(default=django.utils.timezone.now)),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.Designation')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together={('first_name', 'last_name')},
        ),
    ]
