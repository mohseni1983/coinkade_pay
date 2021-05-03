from django.urls import path
from .views import payment, proc_payment, callback

urlpatterns = [
    path('', payment, name='payment'),
    path('pay/', proc_payment, name='proc_payment'),
    path('callback/', callback, name='callback')
]
