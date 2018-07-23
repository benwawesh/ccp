# Generated by Django 2.0.6 on 2018-07-18 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('posts', '0003_auto_20180718_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='voter',
        ),
        migrations.AddField(
            model_name='post',
            name='voter',
            field=models.ManyToManyField(blank=True, to='accounts.WebUser'),
        ),
    ]