from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_device_datetime_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='date_title',
            field=models.CharField(max_length=20, null=True),
        ),
    ]