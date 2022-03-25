from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_device_time_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='datetime_format',
            field=models.CharField(max_length=30, null=True),
        ),
    ]