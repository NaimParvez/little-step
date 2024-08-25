from typing import Any
from django.views import generic

from .models import(
    Category,
    Product,
    Slider
)

class Home(generic.TemplateView):
    template_name ='home.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_categories': Category.objects.filter(featured=True),
            'featured_products': Product.objects.filter(featured=True),
            'sliders': Slider.objects.filter(show=True)
        })
        return context
# Create your views here.

class ProductDetails(generic.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_url_kwarg='slug'

    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        context['related_products']=self.get_object().related
        return context
    
class CategorytDetails(generic.DetailView):
    model = Category
    template_name = 'product/category-details.html'
    slug_url_kwarg='slug'

    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        context['products']=self.get_object().products.all()
        return context

class ProductList(generic.ListView):
    model = Product
    template_name='product/product-list.html'
    context_object_name='object_list'

    def get_context_data(self,**kwargs):
        return super().get_context_data(**kwargs)