from django.shortcuts import render,redirect
from django.views import generic

from .forms import CheckoutForm

from .models import Order,OrderItem
from cart.carts import Cart

class Checkout(generic.View):
    def get(self,*args,**kwargs):
        # order =Order.objects.get(user=self.request.user,paid=False)
        form =CheckoutForm()
        context={
            'form':form,
            'cart':Cart(self.request)
        }
        
        return render(self.request,'order/checkout.html',context)

