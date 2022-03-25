from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_device_date_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='time_title',
            field=models.CharField(max_length=20, null=True),
        ),
    ]