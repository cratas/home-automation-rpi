# Generated by Django 4.0.3 on 2022-03-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_device_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]