# Generated by Django 2.0.6 on 2018-07-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20180718_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='down_vote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='up_vote_count',
            field=models.IntegerField(default=0),
        ),
    ]
