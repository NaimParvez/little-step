from django.views import generic

class Home(generic.TemplateView):
    template_name ='home.html'

# Create your views here.

class ProductDetails(generic.TemplateView):
    template_name = 'product/product-details.html'