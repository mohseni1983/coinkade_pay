# Generated by Django 3.2 on 2021-05-02 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateway', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='createDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 2, 17, 44, 43, 282698), verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='invoice',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='شماره فاکتور'),
        ),
    ]
