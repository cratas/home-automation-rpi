# Generated by Django 4.0.3 on 2022-04-05 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0030_smartdevice'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartdevice',
            name='format',
            field=models.CharField(choices=[('Osvlětlení', 'Light'), ('Topení', 'Heating'), ('Větrák', 'Ventilator')], default=('Osvlětlení', 'Light'), max_length=20),
        ),
    ]