# Generated by Django 2.0 on 2019-03-04 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0002_auto_20190227_1020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joint',
            options={'ordering': ['-date_completed', 'iso']},
        ),
    ]