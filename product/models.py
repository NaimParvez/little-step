from django.conf import settings
from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField( unique=True,max_length=150)
    featured= models.BooleanField(default=False)
    created_data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =['title']
        
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField( unique=True,max_length=250)
    category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
    thumbnail = models.URLField()
    description = models.TextField(null=True,blank=True,default='N/A')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured= models.BooleanField(default=False)
    in_stock=models.BooleanField(default=True)
    # active = models.BooleanField(default=True)
    created_data = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)
    # color = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        ordering =['-id']
        
    def __str__(self) -> str:
        return self.title
    @property
    def related(self):
        return self.category.products.all().exclude(pk=self.pk)
    
class Slider(models.Model):
     title = models.CharField(max_length=50) 
     banner =models.ImageField(upload_to='banners')
     show =models.BooleanField(default=True) 
     created_data = models.DateTimeField(auto_now_add=True)
     
     def __str__(self) -> str:
         return self.title




class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='reviews', 
        on_delete=models.CASCADE,
        null=True,  # Allow null temporarily for migration
        blank=True  # Allow blank in forms
    )
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"} - {self.product.title} - {self.rating}★'