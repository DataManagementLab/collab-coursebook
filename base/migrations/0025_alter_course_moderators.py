# Generated by Django 3.2.20 on 2024-02-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_auto_20240203_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='moderators',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='moderated_courses', to='base.Profile', verbose_name='Moderators'),
        ),
    ]