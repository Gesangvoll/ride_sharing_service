# Generated by Django 2.1.5 on 2019-02-05 06:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0010_auto_20190205_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerrequest',
            name='arrival_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 2, 5, 6, 34, 4, 357263, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='sharerrequest',
            name='destination',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='sharerrequest',
            name='vehicle_type',
            field=models.CharField(choices=[('sedan', 'sedan'), ('suv', 'suv'), ('coupe', 'coupe'), ('van', 'van'), ('hyper', 'hyper')], max_length=6),
        ),
    ]
