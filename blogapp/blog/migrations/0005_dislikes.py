# Generated by Django 2.2.1 on 2019-06-06 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_auto_20190605_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numLikes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogPost')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
