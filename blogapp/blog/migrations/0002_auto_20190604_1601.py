# Generated by Django 2.2.1 on 2019-06-04 22:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='fechaDelPost',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='num_dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='num_likes',
            field=models.IntegerField(default=0),
        ),
    ]
