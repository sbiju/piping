# Generated by Django 2.0 on 2019-03-07 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0004_auto_20190304_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='qc',
            name='fn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='qc',
            name='hardness',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='qc',
            name='hydro',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='qc',
            name='mt_pt',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='MT/PT'),
        ),
        migrations.AddField(
            model_name='qc',
            name='pmi',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='qc',
            name='pneum',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='qc',
            name='rt',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='qc',
            name='visual',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
