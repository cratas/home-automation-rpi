from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_device_communication_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='pulldevice',
            name='delimiter',
            field=models.CharField(max_length=1, default=','),
        ),
    ]