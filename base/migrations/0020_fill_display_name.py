# Generated by Django 3.2.18 on 2023-04-12 17:02

from django.db import migrations


class Migration(migrations.Migration):

    def fill_default_display_name(apps, schema_editor):
        Profile = apps.get_model("base", "Profile")
        for profile in Profile.objects.all():
            profile.display_name = profile.user.username
            profile.save()

    dependencies = [
        ('base', '0019_display_name'),
    ]

    operations = [
        migrations.RunPython(fill_default_display_name, migrations.RunPython.noop)
    ]