# Generated by Django 2.0 on 2019-07-03 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.IntegerField(default=1),
        ),
    ]