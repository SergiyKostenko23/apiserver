# Generated by Django 3.0.6 on 2020-06-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0037_auto_20200612_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]