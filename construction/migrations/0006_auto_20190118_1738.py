# Generated by Django 2.0 on 2019-01-18 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0005_auto_20190118_1737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joint',
            options={'ordering': ['-date_completed']},
        ),
        migrations.AlterModelOptions(
            name='qc',
            options={'ordering': ['-timestamp']},
        ),
    ]
