# Generated by Django 3.2.20 on 2024-02-29 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_content_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='author_message',
            field=models.TextField(blank=True, help_text='The message from the author', verbose_name='Author Message'),
        ),
        migrations.AddField(
            model_name='content',
            name='user_message',
            field=models.TextField(blank=True, help_text='The message from the user', verbose_name='User Message'),
        ),
    ]