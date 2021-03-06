# Generated by Django 4.0.3 on 2022-04-05 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_delete_smartdevice'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmartDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=20, unique=True)),
                ('device_name', models.CharField(max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.room')),
            ],
        ),
    ]
