from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


from cart.models import Coupon



class OrderItem(models.Model):
    product = models.ForeignKey('product.Product',related_name='ordered',on_delete=models.CASCADE)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    quantity =models.PositiveIntegerField(default=1)

    class Meta:
        ordering =['-id']
        
    def __str__(self) -> str:
        return f"{self.product.title} x {self.quatity}"



class Order(models.Model):
    STATUS =('Recieved','On The Way','Delivered')
    
    user =models.ForeignKey(settings.AUTH_USER_MODEL,related_name='order',on_delete=models.CASCADE)
    order_items =models.ManyToManyField(OrderItem)
    coupon =models.ForeignKey(Coupon,null=True,blank=True ,on_delete=models.SET_NULL)
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    email =models.EmailField(max_length=100)
    phone_no =models.CharField(max_length=15)
    address =models.CharField(max_length=250)
    division =models.CharField(max_length=100)
    district =models.CharField(max_length=100)
    upazila =models.CharField(max_length=100)
    total =models.DecimalField(max_digits=10,decimal_places=2)
    paid =models.BooleanField(default=True)
    transaction_id =models.UUIDField()
    status =models.CharField(max_length=20,choices=list(zip(STATUS, STATUS)))
    created_date =models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering =['-created_date']
        
    def __str__(self) -> str:
        return self.first_name + " " + self.last_name