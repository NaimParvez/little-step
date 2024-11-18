from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.carts import Cart
import requests  # Make sure this line is present
from django.conf import settings

class Checkout(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'order/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('order_confirmation')

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        cart = Cart(self.request)
        cart_total = cart.total()['total']
        delivery_charge = self.calculate_delivery_charge(form.initial.get('division', 'Dhaka'))  # Adjust as needed
        total_cost = cart_total + delivery_charge

        context = {
            'form': form,
            'cart': cart,
            'cart_total': cart_total,
            'delivery_charge': delivery_charge,
            'total_cost': total_cost
        }
        return render(self.request, self.template_name, context)

    def form_valid(self, form):
        cart = Cart(self.request)

        # Get form data
        division = form.cleaned_data.get('division')
        delivery_charge = self.calculate_delivery_charge(division)
        cart_total = cart.total()['total']
        total_cost = cart_total + delivery_charge

        # Retrieve selected payment method
        payment_method = self.request.POST.get('payment_method')

        # Handle payment based on method
        if payment_method == 'bkash':
            payment_success = self.process_bkash_payment(total_cost)
        elif payment_method == 'cod':
            # Calculate advance payment (30% of total cost)
            advance_payment = total_cost * 0.30
            # Process advance payment via bKash
            payment_success = self.process_bkash_payment(advance_payment)
        else:
            payment_success = False

        if not payment_success:
            form.add_error(None, "Payment failed. Please try again.")
            return self.form_invalid(form)

        # Save the order
        order = Order.objects.create(
            user=self.request.user,
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            phone_no=form.cleaned_data.get('phone_no'),
            email=form.cleaned_data.get('email'),
            address=form.cleaned_data.get('address'),
            division=division,
            district=form.cleaned_data.get('district'),
            upazila=form.cleaned_data.get('upazila'),
            total_cost=total_cost,
            delivery_charge=delivery_charge,
            payment_method=payment_method
        )
        order.save()

        # Save order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)

        # Initialize default delivery charge (before form submission)
        delivery_charge = 200.00  # Default charge for initial page load
        total_cost = cart.total()['total'] + delivery_charge

        # Update context with cart, delivery charge, and total cost
        context['cart'] = cart
        context['cart_total'] = cart.total()['total']
        context['delivery_charge'] = delivery_charge
        context['total_cost'] = total_cost

        return context

    def calculate_delivery_charge(self, division):
        delivery_charges = {
            'Dhaka': 200.00,
            'Chittagong': 300.00,
            'Rajshahi': 300.00,
            'Khulna': 300.00,
            'Barisal': 300.00,
            'Sylhet': 300.00,
            'Rangpur': 300.00,
            'Mymensingh': 300.00,
        }
        return delivery_charges.get(division, 200.00)

    def process_bkash_payment(self, amount):
        """
        Process bKash payment for the given amount.
        """
        # Step 1: Get the bKash Token
        token_url = f"{settings.BKASH_BASE_URL}/token/grant"
        token_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + settings.BKASH_BASIC_AUTH,
        }
        token_data = {
            'app_key': settings.BKASH_APP_KEY,
            'app_secret': settings.BKASH_APP_SECRET
        }
        try:
            token_response = requests.post(token_url, json=token_data, headers=token_headers)
            token_response.raise_for_status()  # Raise an exception for HTTP errors
            token = token_response.json().get('id_token')

            if not token:
                return False

            # Step 2: Create the Payment
            payment_url = f"{settings.BKASH_BASE_URL}/checkout/create"
            payment_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            payment_data = {
                'amount': str(amount),  # Pass the amount to charge
                'currency': 'BDT',
                'intent': 'sale',
                'merchantInvoiceNumber': f'Inv{self.request.user.id}'  # Unique invoice number for the transaction
            }

            payment_response = requests.post(payment_url, json=payment_data, headers=payment_headers)
            payment_response.raise_for_status()
            payment_info = payment_response.json()

            # Step 3: Check if payment is successful
            if payment_info.get('paymentID'):
                return True  # Payment succeeded
            else:
                return False  # Payment failed
        except requests.RequestException as e:
            print(f"bKash payment error: {e}")
            return False
