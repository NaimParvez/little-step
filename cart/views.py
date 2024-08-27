from django.views import generic
from django.shortcuts import get_object_or_404,redirect
from django.views.generic import TemplateView

from .carts import Cart
from product.models import Product


class AddToCart(generic.View):
    def post(self,*args,**kwargs):
        product =get_object_or_404(Product,id=kwargs.get('product_id'))
        cart =Cart(self.request)
        cart.update(product.id,1)
        return redirect('cart')
    



class CartItems(TemplateView):
    template_name = 'cart/cart.html'
