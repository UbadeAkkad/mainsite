# Generated by Django 4.1.2 on 2023-02-07 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_logging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesslog',
            name='isp',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AddField(
            model_name='accesslog',
            name='location',
            field=models.CharField(default=' / ', max_length=200),
        ),
    ]