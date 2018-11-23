# Generated by Django 2.0 on 2018-11-23 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0020_auto_20181116_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iso',
            name='pipe1',
        ),
        migrations.RemoveField(
            model_name='iso',
            name='pipe2',
        ),
        migrations.RemoveField(
            model_name='iso',
            name='pipe_1l',
        ),
        migrations.RemoveField(
            model_name='iso',
            name='pipe_2l',
        ),
        migrations.AddField(
            model_name='pipe',
            name='material',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
