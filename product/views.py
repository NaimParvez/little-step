from typing import Any
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views import generic

from .forms import ReviewForm
from django.contrib import messages
from django.urls import reverse

from django.core.paginator import(
    PageNotAnInteger,
    EmptyPage,
    InvalidPage,
    Paginator
)
from cart.carts import Cart
from .models import(
    Category,
    Product,
    Slider,
    Review,
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
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related
        context['review_form'] = ReviewForm()
        context['reviews'] = self.get_object().reviews.all()
        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = self.get_object().reviews.filter(user=self.request.user).exists()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to submit a review.')
            return redirect('login')

        product = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            try:
                review.save()
                messages.success(request, 'Your review has been submitted.')
            except:
                messages.error(request, 'You have already reviewed this product.')
        else:
            messages.error(request, 'Error submitting review.')
        
        return redirect(reverse('product-details', kwargs={'slug': product.slug}))
    
class CategorytDetails(generic.DetailView):
    model = Category
    template_name = 'product/category-details.html'
    slug_url_kwarg='slug'

    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        context['products']=self.get_object().products.all()
        return context


class CustomPaginator:
    def __init__(self,request,queryset,paginted_by) -> None:
        self.paginator = Paginator(queryset,paginted_by)
        self.paginated_by = paginted_by
        self.queryset = queryset
        self.page = request.GET.get('page', 1)
        
    def get_queryset(self):
        try:
            queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
            queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset = self.paginator.page(1)
                    
        return queryset
        
        
class ProductList(generic.ListView):
    model = Product
    template_name='product/product-list.html'
    context_object_name='object_list'
    paginate_by=5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add cart items to the context
        cart_items = Cart(self.request)
        context['cart_items'] = cart_items
        
        # Pagination logic
        page_obj = CustomPaginator(self.request, self.get_queryset(), self.paginate_by)
        queryset = page_obj.get_queryset()
        paginator = page_obj.paginator
        
        # Update the context with paginated objects and paginator
        context['object_list'] = queryset
        context['paginator'] = paginator
        
        return context
    
class SearchProducts(generic.View):
     
    def get(self,*args,**kwargs):
        key =self.request.GET.get('key','')
        products= Product.objects.filter(
            Q(title__icontains=key)|
            Q(category__title__icontains=key)
        )
            
        context ={
            'products':products,
            "key":key
        }
        
        return render(self.request,'product/search-products.html',context)
    