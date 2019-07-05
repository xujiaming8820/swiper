# Generated by Django 2.0 on 2019-07-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190703_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('bj', '北京'), ('sz', '深圳'), ('sh', '上海')], max_length=64)),
                ('min_distance', models.IntegerField(default=1)),
                ('max_distance', models.IntegerField(default=10)),
                ('min_dating_age', models.IntegerField(default=18)),
                ('max_dating_age', models.IntegerField(default=81)),
                ('dating_sex', models.IntegerField(default=0)),
                ('vibration', models.BooleanField(default=True)),
                ('only_matche', models.BooleanField(default=True)),
                ('auto_play', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'profiles',
            },
        ),
    ]
