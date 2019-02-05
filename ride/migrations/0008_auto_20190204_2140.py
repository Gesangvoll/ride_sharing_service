# Generated by Django 2.1.5 on 2019-02-05 02:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0007_auto_20190204_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='volume',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='ownerrequest',
            name='arrival_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 5, 2, 40, 7, 869649, tzinfo=utc), null=True),
        ),
    ]