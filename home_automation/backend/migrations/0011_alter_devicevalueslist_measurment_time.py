# Generated by Django 4.0.3 on 2022-03-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_devicevalueslist_measurment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicevalueslist',
            name='measurment_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]