import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import Payment
import http.client
from django.shortcuts import redirect
from datetime import datetime
from telegram.ext import Updater, Dispatcher

updater = Updater('1792589884:AAEcpyJzlOZ-Gaq6ZJqgQgcRaADonOEBfiY')


# msg='سلام\r\n'\
#     'روز بخیر\r\n'\
#     '\r\nمن محسنی هستم\r\n'
# updater.bot.sendMessage('59086635', msg)


# Create your views here.
def bot_message(amount, card, res, ref, name, date, bill, mobile):
    msg = 'یک پرداخت انجام شد:\r\n' \
          '\r\n' \
          f'مبلغ:{amount}' \
          '\r\n' \
          f'پرداخت کننده:{name}' \
          '\r\n' \
          f'شماره کارت:{card}' \
          '\r\n' \
          f'شماره پیگیری:{res}' \
          '\r\n' \
          f'شماره مرجع:{ref}' \
          '\r\n' \
          f'فاکتور:{bill}' \
          '\r\n' \
          f'موبایل:{mobile}' \
          '\r\n' \
          f'تاریخ:{date}' \
          '\r\n' \
          '============='
    updater.bot.sendMessage('59086635', msg)


def payment(request):
    return render(request, 'payment/payform.html', {})


def proc_payment(request):
    baseCallback = request.get_host()
    amount = 0.0
    name = ''
    mobile = ''
    description = ''
    if request.method == "POST":
        amountStr = request.POST["amount"]
        amount = amountStr.replace(',', '')
        name = request.POST["name"]
        mobile = request.POST["mobile"]
        description = request.POST["description"]
    result = Payment.objects.create(mobile=mobile, name=name, description=description, amount=amount)
    print(result)
    url = "https://core.pod.ir/nzh/doServiceCall"
    post = "scProductId=34976&amount={amount}&userId=19505264&billNumber={bill}&wallet=PODLAND_WALLET&redirectUrl" \
           "={callback}/callback"
    payload = post.format(amount=amount, bill=result, callback=baseCallback)
    headers = {
        '_token_': '3d149c1cf78f4b1082e91a2438e83257',
        '_token_issuer_': '1',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    # print(data["hasError"])
    if data["hasError"]:
        return HttpResponse('خطایی در پرداخت رخ داده است')
    redirectUrl = "https://core.pod.ir/nzh/payAnyCreditInvoice?hash={hash}&gateway=PEP".format(hash=data["result"])
    return redirect(redirectUrl)


def callback(request):
    if request.GET:
        billId = request.GET['billNumber']
        invoice = Payment.objects.get(invoice=billId)
        if invoice:
            invoice.cardNo = request.GET['maskedCardNumber']
            invoice.refId = request.GET['tref']
            invoice.rrn = request.GET['rrn']
            invoice.save(update_fields=['cardNo', 'refId', 'rrn'])
            url = "https://core.pod.ir/nzh/doServiceCall"

            payload = 'scProductId=34977&billNumber={bill}'.format(bill=billId)
            headers = {
                '_token_': '3d149c1cf78f4b1082e91a2438e83257',
                '_token_issuer_': '1',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            result = response.json()
            print(result)
            if result['hasError']:
                return HttpResponse('خطایی در پرداخت رخ داده است')
            payment = result['result']
            if payment['payed']:
                invoice = Payment.objects.get(invoice=billId)
                invoice.resId = result['referenceNumber']
                settleDate = datetime.fromtimestamp(int(payment['issuanceDate']) / 1000)
                invoice.paymentDate = settleDate
                invoice.payed = True
                invoice.save(update_fields=['resId', 'paymentDate', 'payed'])
                invoice = Payment.objects.get(invoice=billId)
                bot_message(invoice.amount,invoice.cardNo,invoice.resId,invoice.refId,invoice.name,invoice.createDate,invoice.invoice,invoice.mobile)

                context = {
                    'amount': invoice.amount,
                    'bill': billId,
                    'payed': True,
                    'res': invoice.resId,
                    'ref': invoice.refId,
                    'card': invoice.cardNo,
                    'date': invoice.paymentDate,
                    'name': invoice.name
                }
                return render(request, 'payment/success.html', context)

    return HttpResponse(request.GET)
