# Generated by Django 3.0.6 on 2020-06-08 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0012_auto_20200608_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='asd\\videos/'),
        ),
    ]