# Generated by Django 3.0.5 on 2020-06-18 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_clickdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='clickdetail',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 18, 21, 25, 11, 156379), verbose_name='date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clickdetail',
            name='userType',
            field=models.CharField(default='NA', max_length=20),
        ),
    ]
