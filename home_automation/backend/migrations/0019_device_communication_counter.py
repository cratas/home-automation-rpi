from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_device_communication_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='communication_counter',
            field=models.IntegerField(default=0),
        ),
    ]