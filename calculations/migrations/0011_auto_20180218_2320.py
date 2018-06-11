# Generated by Django 2.0 on 2018-02-18 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calculations', '0010_auto_20180218_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='designer', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='designer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='materialdata',
            name='designer',
        ),
        migrations.RemoveField(
            model_name='materialdata',
            name='purchaser',
        ),
        migrations.RemoveField(
            model_name='materialdata',
            name='user',
        ),
        migrations.DeleteModel(
            name='Designer',
        ),
        migrations.AddField(
            model_name='materialdata',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='calculations.Owner'),
            preserve_default=False,
        ),
    ]
