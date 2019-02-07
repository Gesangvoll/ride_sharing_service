# Generated by Django 2.1.5 on 2019-02-07 06:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerrequest',
            name='arrival_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 7, 6, 38, 13, 472080, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='ownerrequest',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sharerrequest',
            name='earliest_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 7, 6, 38, 13, 472702, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='sharerrequest',
            name='latest_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 7, 6, 38, 13, 472740, tzinfo=utc), null=True),
        ),
    ]
