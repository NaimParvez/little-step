from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField( unique=True)
    featured= models.BooleanField(default=False)
    created_data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering =['title']
        
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField( unique=True)
    category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
    thumbnail = models.URLField()
    description = models.TextField(null=True,blank=True,default='N/A')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured= models.BooleanField(default=False)
    # active = models.BooleanField(default=True)
    created_data = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =['-id']
        
    def __str__(self) -> str:
        return self.title
    
    
class Slider(models.Model):
     title = models.CharField(max_length=50) 
     banner =models.ImageField(upload_to='banners')
     show =models.BooleanField(default=True) 
     created_data = models.DateTimeField(auto_now_add=True)
     
     def __str__(self) -> str:
         return self.title