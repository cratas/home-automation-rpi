from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_pulldevice_delimiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='datetime_title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]