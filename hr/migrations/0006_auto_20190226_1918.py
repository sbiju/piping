# Generated by Django 2.0 on 2019-02-26 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_auto_20190226_1812'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyreport',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterUniqueTogether(
            name='dailyreport',
            unique_together={('employee', 'timestamp')},
        ),
    ]
