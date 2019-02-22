# Generated by Django 2.0 on 2019-02-15 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0018_auto_20190208_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErectionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
