from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_alter_devicevalueslist_measurment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='has_error',
            field=models.BooleanField(default=False),
        ),
    ]