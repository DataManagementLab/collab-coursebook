# Generated by Django 3.2.20 on 2024-02-15 23:44

import content.mixin
import content.validator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20240215_2344'),
        ('content', '0014_panoptovideocontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseContent',
            fields=[
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.content', verbose_name='Content')),
                ('source', models.TextField(verbose_name='Source')),
                ('license', models.CharField(blank=True, max_length=200, verbose_name='License')),
                ('tasks', models.FileField(blank=True, upload_to='uploads/contents/%Y/%m/%d/', validators=[content.validator.Validator.validate_pdf], verbose_name='Tasks')),
                ('solutions', models.FileField(blank=True, upload_to='uploads/contents/%Y/%m/%d/', validators=[content.validator.Validator.validate_pdf], verbose_name='Solutions')),
            ],
            options={
                'verbose_name': 'Exercise Content',
                'verbose_name_plural': 'Exercise Contents',
            },
            bases=(models.Model, content.mixin.GeneratePreviewMixin),
        ),
    ]
