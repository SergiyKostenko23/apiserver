# Generated by Django 3.0.6 on 2020-06-15 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0038_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='criado_por',
            field=models.IntegerField(),
        ),
    ]