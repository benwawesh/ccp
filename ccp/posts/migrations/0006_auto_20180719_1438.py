# Generated by Django 2.0.6 on 2018-07-19 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20180719_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='voter',
            field=models.ManyToManyField(related_name='voter', to=settings.AUTH_USER_MODEL),
        ),
    ]
