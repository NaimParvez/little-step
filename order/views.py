from django.shortcuts import render,redirect
from django.views import generic



from .models import Order,OrderItem


class Checkout(generic.View):
    def get(self,*args,**kwargs):
        # order =Order.objects.get(user=self.request.user,paid=False)
        return render(self.request,'order/checkout.html')

