# Generated by Django 3.0.6 on 2020-05-09 16:00

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_disability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='disability',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('PD', '지체 장애'), ('VD', '시각 장애'), ('AD', '청각 장애'), ('W/B', '영유아 동반'), ('NO', '해당 없음')], max_length=15, null=True),
        ),
    ]
