import weasyprint

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string

from cart.cart import Cart
from .forms import OrderCreateForm
from .tasks import order_created
from .models import OrderItem, Order

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('pdf.css'))]
    )
    return response

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, 
        'admin/orders/order/detail.html',
        {
            'order': order
        }
    )

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            
            order.save()
    
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            #set the order in the session
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm()

        return render(
            request,
            'orders/order/create.html',
            {
                'cart': cart,
                'form': form
            }
        )
