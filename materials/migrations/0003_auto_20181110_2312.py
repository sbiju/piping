# Generated by Django 2.0 on 2018-11-10 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_material'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='materialdata',
            unique_together=set(),
        ),
    ]