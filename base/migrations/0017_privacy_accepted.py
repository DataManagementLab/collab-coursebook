# Generated by Django 3.2.5 on 2021-07-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20210302_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='accepted_privacy_note',
            field=models.BooleanField(blank=True, default=False, verbose_name='Accepted privacy note?'),
        ),
    ]
