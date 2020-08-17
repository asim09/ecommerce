from .models import Order

def cartItems(request):
    shipping_info = False
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        for i in items:
            if not i.product.digital:
                shipping_info = True
    else:
        order = {'get_cart_items': 0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
    context = {
        'cartItems':cartItems,
        'shipping':shipping_info
    }
    return {'cartItems':cartItems,'shipping':shipping_info}
