# Generated by Django 3.0.4 on 2020-04-05 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                       to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, verbose_name='Biography')),
            ],
        ),
    ]
