# Generated by Django 2.0 on 2019-02-25 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0021_auto_20190225_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joint',
            name='welder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='welder', to='hr.Employee'),
        ),
    ]