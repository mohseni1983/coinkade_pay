from django.db import models
from django.contrib import admin
import datetime
import random


class Payment(models.Model):
    invoice = models.BigIntegerField(verbose_name='شماره فاکتور',  blank=True, null=True,)

    name = models.CharField(max_length=50, verbose_name='نام و نام خانوادگی', blank=False)
    mobile = models.CharField(max_length=15, verbose_name='شماره همراه', blank=False)
    amount = models.DecimalField(verbose_name='مبلغ', blank=False, decimal_places=2, max_digits=12)
    description = models.CharField(verbose_name='توضیحات', max_length=300, null=True, blank=True)
    payed = models.BooleanField(default=False, verbose_name='پرداخت شده؟')
    createDate = models.DateTimeField(default=datetime.datetime.now(), verbose_name='تاریخ ایجاد')
    paymentDate = models.DateTimeField(verbose_name='تاریخ پرداخت', null=True, blank=True)
    rrn = models.CharField(verbose_name='RRN', max_length=250, null=True, blank=True)
    refId = models.CharField(verbose_name='شماره پیگیری', max_length=250, null=True, blank=True)
    resId = models.CharField(verbose_name='شناسه پرداخت', max_length=250, null=True, blank=True)
    cardNo = models.CharField(verbose_name='شماره کارت', max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.invoice)

    class Meta:
        verbose_name = 'پرداخت ها'
        verbose_name_plural = 'پرداخت ها'

    def save(self, *args, **kwargs):
        self.invoice = int(self.mobile + str(random.randint(10000,99999)))
        super().save(*args, **kwargs)  # Call the "real" save() method.
        return self.invoice



class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','payed', 'invoice', 'amount', 'name', 'mobile']
    list_filter = ['invoice','payed', 'refId', 'resId', 'mobile', 'name']
    search_fields = ['invoice', 'refId', 'resId', 'mobile', 'name']
    readonly_fields = ['invoice','refId', 'resId']


admin.site.register(Payment, PaymentAdmin)
