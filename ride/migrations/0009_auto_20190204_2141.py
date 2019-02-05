# Generated by Django 2.1.5 on 2019-02-05 02:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0008_auto_20190204_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerrequest',
            name='arrival_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 5, 2, 41, 2, 4627, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='volume',
            field=models.IntegerField(),
        ),
    ]