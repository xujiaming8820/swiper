# Generated by Django 2.0 on 2019-07-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0003_auto_20190708_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vip',
            name='level',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
