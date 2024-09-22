from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.carts import Cart

class Checkout(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'order/checkout.html'  # Add this to specify the template for rendering
    form_class = CheckoutForm
    success_url = reverse_lazy('order_confirmation')  # Redirect after successful form submission

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        cart = Cart(self.request)
        context = {
            'form': form,
            'cart': cart,
            'cart_total': cart.total()['total'],  # Getting the total from the cart
            'delivery_charge': 0  # Initialize with 0, will update on form submission
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

        # Process payment
        payment_success = self.process_payment(payment_method, total_cost)

        if not payment_success:
            # Handle payment failure (show error, log the issue, etc.)
            form.add_error(None, "Payment failed. Please try again.")
            return self.form_invalid(form)

        # Save the order if payment was successful
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

        # You can save the order items here if needed
        # Example: 
        # for item in cart:
        #     OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], subtotal=item['subtotal'])

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
        # Define delivery charges based on division
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
        return delivery_charges.get(division, 200.00)  # Default charge if division not found

    def process_payment(self, payment_method, total_cost):
        """
        Process the payment based on the selected payment method.
        Returns True if payment is successful, False otherwise.
        """
        if payment_method == 'paypal':
            # Process PayPal payment (integrate with PayPal API)
            return self.process_paypal_payment(total_cost)
        elif payment_method == 'credit_card':
            # Process Credit Card payment (integrate with Stripe, etc.)
            return self.process_credit_card_payment(total_cost)
        elif payment_method == 'cod':
            # Cash on Delivery doesn't need actual payment processing
            return True
        else:
            # Unsupported payment method
            return False

    def process_paypal_payment(self, total_cost):
        # Integrate PayPal API here
        # Example pseudo-code for PayPal:
        # response = paypal_api.make_payment(total_cost)
        # return response['status'] == 'success'
        return True  # Simulate success

    def process_credit_card_payment(self, total_cost):
        # Integrate credit card payment gateway (like Stripe)
        # Example pseudo-code for Stripe:
        # response = stripe_api.charge_card(total_cost)
        # return response['status'] == 'success'
        return True  # Simulate success
