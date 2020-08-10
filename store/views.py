from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'store/store.html',context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        for i in items:
            print(i.id,i.product,i.product_id,i.quantity)
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}

    context = {
        'items': items,
        'order': order
    }
    # for i in context['items']:
    #     print(i.id,i.product,i.quantity)

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    print(productId)
    product = Product.objects.get(id=productId)
    print('-------------',product)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
    print(orderItem)
    if action == 'add':
        print('----2----')
        print(orderItem.product_id,orderItem.quantity)
        print('----2----')
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        print('----2----')
        print(orderItem.product_id,orderItem.quantity)
        print('----2----')
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('This item is added',safe=False)
