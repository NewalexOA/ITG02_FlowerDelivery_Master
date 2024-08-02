from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, ReviewForm, OrderForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Review, Cart, CartItem, OrderItem
from django.db.models import Sum, F

def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    can_review = False
    user_orders = Order.objects.filter(user=request.user, status='Completed')
    for order in user_orders:
        if OrderItem.objects.filter(order=order, product=product).exists():
            can_review = True
            break
    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'core/product_detail.html', {'product': product, 'reviews': reviews, 'form': form, 'can_review': can_review})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        print("New cart item created:", cart_item)
    print("Cart:", cart)
    print("Cart items:", cart.items.all())
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, pk):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product__pk=pk)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'core/cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            address=request.POST['address'],
            phone=request.POST['phone']
        )
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.items.all().delete()
        return redirect('order_history')
    return render(request, 'core/checkout.html', {'cart': cart})


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'core/signup.html'

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'core/order_history.html', {'orders': orders})

@login_required
def order_analytics(request):
    total_sales = OrderItem.objects.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0
    total_orders = Order.objects.count()
    sales_by_month = OrderItem.objects.values('order__created_at__month').annotate(total=Sum(F('quantity') * F('product__price'))).order_by('order__created_at__month')
    sales_by_product = Product.objects.annotate(total_sales=Sum('orderitem__quantity')).order_by('-total_sales')

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_month': sales_by_month,
        'sales_by_product': sales_by_product,
    }
    return render(request, 'core/order_analytics.html', context)
