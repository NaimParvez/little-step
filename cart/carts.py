from django.conf import settings
from .models import Coupon
from product.models import Product



class Cart(object):
    def __init__(self,request) ->None:
        self.session= request.session
        self.cart_id =settings.CART_ID
        self.coupon_id=settings.COUPON_ID
        cart=self.session.get(self.cart_id)
        coupon=self.session.get(self.coupon_id)
        self.cart=self.session[self.cart_id]= cart if cart else {}
        self.coupon=self.session[self.coupon_id]= coupon if coupon else None
        
    def update(self,product_id,quantity=1):
        product =Product.objects.get(id=product_id)
        self.session[self.cart_id].setdefault(str(product_id),{"quantity": 0 })
        updated_quantity=self.session[self.cart_id][str(product_id)]['quantity']+ quantity
        self.session[self.cart_id][str(product_id)]['quantity']=updated_quantity
        self.session[self.cart_id][str(product_id)]['subtotal']=updated_quantity*float(product.price)

        if updated_quantity <1 :
            del self.session[self.cart_id][str(product_id)]

        self.save()

    def add_coupon(self , coupon_id):
        self.session[self.coupon_id]= coupon_id
        self.save()



    def __iter__(self):
        products =Product.objects.filter(id__in=list(self.cart.keys()))
        cart=self.cart.copy()

        for item in products:
            product =Product.objects.get(id=item.id)
            cart[str(item.id)]['product']={
                "id": item.id,
                "title": item.title,
                "category":item.category.title,
                "price":float(item.price),
                "thumbnail":item.thumbnail,
                "slug": item.slug
            }
            yield cart[str(item.id)]

    def save(self):
        self.session.modified =True

    def __len__(self):
        return len(list(self.cart.keys()))
    
    def clear(self):
        try:
            del self.session[self.cart_id]
            del self.session[self.coupon_id]
        except:
            pass
        self.save
        
    def restore_after_logout(self,cart={},coupon=None):
        self.cart=self.session[self.cart_id]=cart
        self.coupon=self.session[self.coupon_id]=coupon
        self.save()
    
    def total(self):
           # Calculate the sum of subtotals in the cart
        amount = sum(product['subtotal'] for product in self.cart.values())
        before_discount = amount

        discount = 0
        discount_amount = 0
        
        # Check if a coupon is applied
        if self.coupon:
           try:
            # Get the coupon object
              coupon = Coupon.objects.get(id=self.coupon)

            # Check if the total amount meets the required amount for the coupon
              if before_discount >= coupon.required_amount_to_use_coupon:
                # Apply the discount
                discount = coupon.discount
                discount_amount = before_discount * (discount / 100)
                # Deduct discount from total
                amount -= discount_amount
              else:
                # If total is below required amount, clear the coupon
                self.clear_coupon()

           except Coupon.DoesNotExist:
                discount = 0  # No discount if coupon doesn't exist

        # Return the total amount after discount, original amount, and discount percentage
        return {
            'total': round(amount,2),
            'before_discount': round(before_discount,2),
            'discount': round(discount,2),  # Percentage
            'discount_amount': round(discount_amount,2)  # Discount in taka
        }

    def clear_coupon(self):
    # """Clear the applied coupon if it no longer qualifies."""
        self.session[self.coupon_id] = None
        self.save()