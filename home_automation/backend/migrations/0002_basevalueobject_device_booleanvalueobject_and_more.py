# Generated by Django 4.0.3 on 2022-03-16 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseValueObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_title', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=20, unique=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='BooleanValueObject',
            fields=[
                ('basevalueobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.basevalueobject')),
                ('value', models.BooleanField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.basevalueobject',),
        ),
        migrations.CreateModel(
            name='NumericValueObject',
            fields=[
                ('basevalueobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.basevalueobject')),
                ('value', models.DecimalField(decimal_places=3, max_digits=10)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.basevalueobject',),
        ),
        migrations.CreateModel(
            name='PullDevice',
            fields=[
                ('device_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.device')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.device',),
        ),
        migrations.CreateModel(
            name='PushDevice',
            fields=[
                ('device_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.device')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.device',),
        ),
        migrations.CreateModel(
            name='StringValueObject',
            fields=[
                ('basevalueobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.basevalueobject')),
                ('value', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.basevalueobject',),
        ),
        migrations.CreateModel(
            name='DeviceValuesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.device')),
            ],
        ),
        migrations.AddField(
            model_name='basevalueobject',
            name='device_values',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.devicevalueslist'),
        ),
        migrations.AddField(
            model_name='basevalueobject',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype'),
        ),
    ]
