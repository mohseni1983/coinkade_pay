# Generated by Django 3.2 on 2021-05-02 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateway', '0002_auto_20210502_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 50, 59, 149516), verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='invoice',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='شماره فاکتور'),
        ),
    ]
