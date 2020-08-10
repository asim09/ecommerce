from .models import Order

def cartItems(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {
        'cartItems':cartItems
    }
    return {'cartItems':cartItems}
