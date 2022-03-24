from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_device_has_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='communication_interval',
            field=models.IntegerField(default=1),
        ),
    ]