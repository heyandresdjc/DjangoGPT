# Generated by Django 5.1 on 2024-08-12 01:01

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingfile',
            name='is_ran',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trainingfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='training/%Y/%m/%d'), upload_to=''),
        ),
    ]