# Generated by Django 2.0 on 2019-02-27 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_centre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bolt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Quantity in Nos')),
            ],
        ),
        migrations.CreateModel(
            name='BoltGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FitUpStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FlangeClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Gasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Quantity in Nos')),
                ('gasket_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.FlangeClass')),
            ],
        ),
        migrations.CreateModel(
            name='GasketMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Pefs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Spool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spool_tag', models.CharField(blank=True, max_length=120, null=True)),
                ('timestamp', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpoolStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WeldStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='iso',
            options={'ordering': ['service__name']},
        ),
        migrations.AlterModelOptions(
            name='lineclass',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='lineclass',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project'),
        ),
        migrations.AddField(
            model_name='material',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project'),
        ),
        migrations.AddField(
            model_name='service',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project'),
        ),
        migrations.AddField(
            model_name='size',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='lineclass',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='material',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='size',
            unique_together={('project', 'name')},
        ),
        migrations.AddField(
            model_name='spool',
            name='iso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Iso'),
        ),
        migrations.AddField(
            model_name='spool',
            name='spool_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.SpoolStatus'),
        ),
        migrations.AddField(
            model_name='gasket',
            name='gasket_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.GasketMaterial'),
        ),
        migrations.AddField(
            model_name='gasket',
            name='iso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Iso'),
        ),
        migrations.AddField(
            model_name='gasket',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Size'),
        ),
        migrations.AddField(
            model_name='bolt',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.BoltGrade'),
        ),
        migrations.AddField(
            model_name='bolt',
            name='iso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Iso'),
        ),
        migrations.AddField(
            model_name='bolt',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Size'),
        ),
        migrations.AddField(
            model_name='flange',
            name='flange_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.FlangeClass'),
        ),
        migrations.AddField(
            model_name='iso',
            name='pefs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='control_centre.Pefs'),
        ),
        migrations.AlterUniqueTogether(
            name='spoolstatus',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='gasketmaterial',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='flangeclass',
            unique_together={('project', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='boltgrade',
            unique_together={('project', 'name')},
        ),
    ]
