# Generated by Django 3.0.6 on 2020-06-08 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0024_auto_20200608_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='C:\\Users\\sergy.kostenko\\Desktop\\apiserver\\server\\media\\videos'),
        ),
    ]