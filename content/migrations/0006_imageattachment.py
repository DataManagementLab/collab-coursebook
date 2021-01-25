# Generated by Django 3.0.7 on 2021-01-24 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_favorite'),
        ('content', '0005_auto_20200729_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAttachment',
            fields=[
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.Content', verbose_name='Content')),
                ('image', models.ImageField(upload_to='uploads/contents/%Y/%m/%d/', verbose_name='Image Attachment')),
                ('source', models.TextField(verbose_name='Source')),
                ('license', models.CharField(blank=True, max_length=200, verbose_name='License')),
            ],
            options={
                'verbose_name': 'Image Attachment in Content',
                'verbose_name_plural': 'Image Attachments in Content',
            },
        ),
    ]
