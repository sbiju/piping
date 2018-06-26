# Generated by Django 2.0 on 2018-06-23 05:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('control_centre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('size', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unit', models.CharField(choices=[('Nos', 'Nos'), ('Mtr', 'Mtr')], default='Nos', max_length=20)),
                ('quantity_purchased', models.IntegerField(blank=True, null=True)),
                ('balance_purchase', models.IntegerField(blank=True, null=True, verbose_name='Balance to be Purchased')),
                ('quantity_issued', models.IntegerField(blank=True, null=True)),
                ('balance_issue', models.IntegerField(blank=True, null=True, verbose_name='Balance to be Issued')),
                ('quantity_used', models.IntegerField(blank=True, null=True)),
                ('balance_used', models.IntegerField(blank=True, null=True, verbose_name='Balance to be Used')),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('purchased', models.BooleanField(default=False)),
                ('fabricated', models.BooleanField(default=False)),
                ('issued', models.BooleanField(default=False)),
                ('date_entered', models.DateField(default=django.utils.timezone.now)),
                ('date_purchased', models.DateField(default=django.utils.timezone.now)),
                ('date_issued', models.DateField(default=django.utils.timezone.now)),
                ('date_fabricated', models.DateField(default=django.utils.timezone.now)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='Price Paid')),
                ('iso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_centre.Iso')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='materialdata',
            unique_together={('iso', 'name', 'size')},
        ),
    ]
