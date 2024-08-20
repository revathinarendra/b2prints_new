from django.core import signing
from django.views.generic.edit import FormView
from .models import Order
from .forms import OrderForm
from django.shortcuts import  redirect,render, get_object_or_404



class OrderCreateView(FormView):
    template_name = 'order_form.html'
    form_class = OrderForm

    def form_valid(self, form):
        print('Form is valid, about to save the form')
        order = form.save(commit=False)
        print(f'Order before saving: {order}')
        order.save()
        print(f'Order saved with ID: {order.order_id}')

        # Encrypt the order_id
        encrypted_order_id = signing.dumps(order.order_id)

        return redirect('order_success', order_id=encrypted_order_id)

    def form_invalid(self, form):
        print('Form is invalid')
        print(f'Errors: {form.errors}')
        return super().form_invalid(form)


def order_success(request, order_id):
    print('Entered order_success view')

    # Decrypt the order_id
    try:
        decrypted_order_id = signing.loads(order_id)
    except signing.BadSignature:
        # Handle the case where the signature is tampered with or invalid
        return render(request, 'error.html', {'message': 'Invalid order ID'})

    order = get_object_or_404(Order, order_id=decrypted_order_id)
    print(f'Order retrieved: {order}')

    context = {
        'order': order
    }

    return render(request, 'order_success.html', context)
