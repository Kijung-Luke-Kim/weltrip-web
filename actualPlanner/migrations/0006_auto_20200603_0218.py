# Generated by Django 3.0.5 on 2020-06-02 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actualPlanner', '0005_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='userId',
            new_name='userRated',
        ),
    ]
