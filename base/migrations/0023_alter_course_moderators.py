# Generated by Django 3.2.20 on 2024-02-03 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20240201_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='moderators',
            field=models.ManyToManyField(related_name='course_moderators', to='base.Profile', verbose_name='Moderators'),
        ),
    ]