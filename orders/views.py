from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Order
from .forms import OrderForm
# views.py

from django.views.generic.edit import FormView
from django.shortcuts import redirect
from .models import Order
from .forms import OrderForm
from .utils.file_upload import upload_file  # Import your file upload function

class OrderCreateView(FormView):
    template_name = 'order_form.html'
    form_class = OrderForm

    def form_valid(self, form):
        print('Form is valid, about to save the form')
        order = form.save(commit=False)
        
        # Handle file uploads
        front_image_file = self.request.FILES.get('front_side_image')
        back_image_file = self.request.FILES.get('back_side_image')
        
        if front_image_file:
            path = f'orders/{front_image_file.name}'
            result = upload_file(front_image_file, path)
            if result:
                order.front_side_image_url = result['data']['Key']
        
        if back_image_file:
            path = f'orders/{back_image_file.name}'
            result = upload_file(back_image_file, path)
            if result:
                order.back_side_image_url = result['data']['Key']
        
        order.save()
        print(f'Order saved with ID: {order.order_id}')
        return redirect('order_success', order_id=order.order_id)
    
    def form_invalid(self, form):
        print('Form is invalid')
        print(f'Errors: {form.errors}')
        return super().form_invalid(form)




from django.shortcuts import render, get_object_or_404
from .models import Order

def order_success(request, order_id):
    print('Entered order_success view')
    order = get_object_or_404(Order, order_id=order_id)
    print(f'Order retrieved: {order}')

    context = {
        'order': order
    }

    return render(request, 'order_success.html', context)
