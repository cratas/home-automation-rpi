# Generated by Django 4.0.3 on 2022-03-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_device_error_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]