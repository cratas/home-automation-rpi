# Generated by Django 4.0.3 on 2022-03-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_merge_20220325_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pulldevice',
            name='format',
            field=models.CharField(choices=[('csv', 'Csv'), ('parametres', 'Parametres')], default=('csv', 'Csv'), max_length=20),
        ),
    ]
