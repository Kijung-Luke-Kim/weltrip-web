# Generated by Django 3.0.5 on 2020-05-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actualPlanner', '0003_auto_20200527_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='planner',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='planner',
            name='user',
            field=models.CharField(max_length=20),
        ),
    ]
