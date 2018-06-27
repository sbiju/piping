# Generated by Django 2.0 on 2018-06-27 05:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('content', models.TextField()),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
