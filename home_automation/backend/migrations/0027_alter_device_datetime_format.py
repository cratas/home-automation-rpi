# Generated by Django 4.0.3 on 2022-03-25 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0026_alter_pulldevice_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='datetime_format',
            field=models.CharField(default='%Y-%m-%d %H:%M:%S', max_length=30),
        ),
    ]
