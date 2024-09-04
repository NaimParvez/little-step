from datetime import datetime
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404,redirect
from django.views.generic import TemplateView

from .carts import Cart
from .models import Coupon
from product.models import Product


class AddToCart(generic.View):
    def post(self,*args,**kwargs):
        product =get_object_or_404(Product,id=kwargs.get('product_id'))
        cart =Cart(self.request)
        cart.update(product.id,1)
        return redirect('cart')
    



class CartItems(generic.TemplateView):
    template_name = 'cart/cart.html'
  
    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        clear = request.GET.get('clear', False)
        cart = Cart(request)
        
        # Ensure product_id and quantity are present and valid
        if product_id and quantity:
            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                messages.error(request, "Invalid quantity provided.")
                return redirect('cart')
            
            if quantity > 0:
                product = get_object_or_404(Product, id=product_id)
                if product.in_stock:
                    cart.update(int(product_id), quantity)
                else:
                    messages.warning(request, "The product is not in stock anymore.")
            else:
                messages.warning(request, "Quantity must be greater than zero.")
            return redirect('cart')
        
        # Clear the cart if requested
        if clear:
            cart.clear()
            return redirect('cart')

        # Default behavior: return the template view
        return super().get(request, *args, **kwargs)
      
class AddCoupon(generic.View):
    def post(self,*args,**kwargs):
        code=self.request.POST.get('coupon', '')
        coupon= Coupon.objects.filter(code_iexact=code,active=True)
        cart =Cart(self.request)


        if coupon.exists():
            coupon = coupon.first()
            current_time = datetime.date(timezone.now())
            active_date=coupon.active_date
            expiry_date = coupon.expiry_date
            if current_time > expiry_date:
                messages.warning(self.request,"The coupon expired")
                return redirect('cart')
            if current_time < active_date:
                messages.warning(self.request,"The coupon is yet to be available")
                return redirect('cart')
                
            if cart.total() < coupon.required_amount_to_use_coupon:
                messages.warning(self.request,f"You have to shop at least {coupon.required_amount_to_use_coupon}to use this coupon code")
                return redirect('cart')
                
            cart.add_coupon(coupon.id)
            messages.success(self.request,"Your coupon has been included successfully !")
            return redirect('cart')
        else:
            messages.warning(self.request,"Invalid coupon code")
            return redirect('cart')