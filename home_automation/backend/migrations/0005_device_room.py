# Generated by Django 4.0.3 on 2022-03-18 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_pulldevice_source_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.room'),
        ),
    ]
