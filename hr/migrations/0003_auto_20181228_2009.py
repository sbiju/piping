# Generated by Django 2.0 on 2018-12-28 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20181228_2007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['first_name']},
        ),
    ]
