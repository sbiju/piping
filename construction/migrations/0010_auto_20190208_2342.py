# Generated by Django 2.0 on 2019-02-08 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0009_auto_20190118_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joint',
            name='erection_status',
            field=models.CharField(blank=True, choices=[('Erected', 'Erected'), ('Pending', 'Pending')], max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='qc',
            name='status',
            field=models.CharField(choices=[('Erected', 'Erected'), ('Pending', 'Pending')], default='Pending', max_length=40, verbose_name='Joint Status'),
        ),
    ]
