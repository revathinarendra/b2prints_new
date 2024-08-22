from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core import signing
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from .models import Order
from .forms import OrderForm


# class OrderCreateView(FormView):
#     template_name = 'order_form.html'
#     form_class = OrderForm

#     def form_valid(self, form):
#         print('Form is valid, about to save the form')
#         order = form.save(commit=False)
#         print(f'Order before saving: {order}')
#         order.save()
#         print(f'Order saved with ID: {order.order_id}')

#         # Encrypt the order_id
#         encrypted_order_id = signing.dumps(order.order_id)

#         # Send email if email address is provided
#         if order.email:
#             current_site = get_current_site(self.request)
#             domain = current_site.domain
#             order_success_url = f'http://{domain}{self.request.build_absolute_uri(redirect("order_success", order_id=encrypted_order_id).url)}'
#             subject = 'Your Order Details'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [order.email]

#             # Render the email template with context
#             email_context = {
#                 'printer_name': order.printer_name,
#                 'order_success_url': order_success_url,
#             }
#             email_body = render_to_string('order_success_email.html', email_context)

#             # Send the email
#             email = EmailMultiAlternatives(subject, email_body, from_email, recipient_list)
#             email.attach_alternative(email_body, "text/html")
#             email.send()

#         return redirect('order_success', order_id=encrypted_order_id)

#     def form_invalid(self, form):
#         print('Form is invalid')
#         print(f'Errors: {form.errors}')
#         return super().form_invalid(form)


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

        # Send email if email address is provided
        if order.email:
            current_site = get_current_site(self.request)
            domain = current_site.domain
            # Construct the order success URL without prepending the domain again
            order_success_url = self.request.build_absolute_uri(
                redirect('order_success', order_id=encrypted_order_id).url
            )
            subject = 'Your Order Details'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.email]

            # Render the email template with context
            email_context = {
                'printer_name': order.printer_name,
                'order_success_url': order_success_url,
            }
            email_body = render_to_string('order_success_email.html', email_context)

            # Send the email
            email = EmailMultiAlternatives(subject, email_body, from_email, recipient_list)
            email.attach_alternative(email_body, "text/html")
            email.send()

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
