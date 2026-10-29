from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction, models
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, OrderItem, Wishlist, Review


def cart_data(request):
    c = request.session.get('cart', {})
    items = []
    total = Decimal('0')
    for p in Product.objects.filter(id__in=c.keys()):
        q = int(c.get(str(p.id), 0))
        sub = p.price * q
        if q > 0:
            items.append({'product': p, 'quantity': q, 'subtotal': sub})
            total += sub
    return items, total


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        u = request.POST.get('username', '').strip()
        e = request.POST.get('email', '').strip()
        p = request.POST.get('password', '')
        cp = request.POST.get('confirm_password', '')
        if not u or not e or not p:
            messages.error(request, 'Please fill in all fields.')
        elif p != cp:
            messages.error(request, 'Passwords do not match.')
        elif len(p) < 6:
            messages.error(request, 'Password must contain at least 6 characters.')
        elif User.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists. Please login or choose another username.')
        elif User.objects.filter(email=e).exists():
            messages.error(request, 'An account with this email already exists. Please login instead.')
        else:
            user = User.objects.create_user(username=u, email=e, password=p)
            login(request, user)
            messages.success(request, f'Welcome to Urs Cart, {u}! Your account is ready.')
            return redirect('home')
    return render(request, 'registration/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next') or 'home')
        messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'registration/login.html')


@login_required
def home(request):
    products = Product.objects.all().order_by('-id')
    saved_categories = Wishlist.objects.filter(user=request.user).values_list('product__category', flat=True)
    if saved_categories:
        recommended = Product.objects.filter(category__in=saved_categories).exclude(id__in=Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)).annotate(review_count=models.Count('reviews')).order_by('-review_count','-id')[:4]
    else:
        recommended = Product.objects.annotate(review_count=models.Count('reviews')).order_by('-review_count','-id')[:4]
    return render(request, 'store/home.html', {
        'featured': products[:8],
        'categories': Product.objects.values_list('category', flat=True).distinct(),
        'smart_recommendations': recommended,
    })


@login_required
def shop(request):
    cat = request.GET.get('category', '')
    ps = Product.objects.all().order_by('-id')
    if cat:
        ps = ps.filter(category__iexact=cat)
    return render(request, 'store/shop.html', {
        'products': ps,
        'categories': Product.objects.values_list('category', flat=True).distinct(),
        'active_category': cat,
    })


@login_required
def categories(request):
    categories_data = []
    for c in Product.objects.values_list('category', flat=True).distinct():
        first = Product.objects.filter(category=c).order_by('id').first()
        categories_data.append((c, Product.objects.filter(category=c).count(), first))
    return render(request, 'store/categories.html', {'categories': categories_data})


@login_required
def about(request):
    return render(request, 'store/about.html')


@login_required
def product_detail(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    related = Product.objects.filter(category=p.category).exclude(id=p.id).annotate(review_count=models.Count('reviews')).order_by('-review_count','-id')[:4]
    reviews = p.reviews.select_related('user').all()[:6]
    avg = p.reviews.aggregate(avg=models.Avg('rating')).get('avg')
    return render(request, 'store/product_detail.html', {
        'product': p,
        'related': related,
        'reviews': reviews,
        'review_average': round(avg,1) if avg else None,
        'review_count': p.reviews.count(),
        'in_wishlist': Wishlist.objects.filter(user=request.user, product=p).exists(),
        'my_review': p.reviews.filter(user=request.user).first(),
    })


@login_required
def add_to_cart(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    c = request.session.get('cart', {})
    k = str(p.id)
    q = int(c.get(k, 0))
    if q < p.stock:
        c[k] = q + 1
        request.session['cart'] = c
        messages.success(request, f'{p.name} added to cart.')
    else:
        messages.warning(request, 'Maximum available stock reached.')
    return redirect(request.POST.get('next') or 'cart')


@login_required
def cart(request):
    items, total = cart_data(request)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


@login_required
def update_cart(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    c = request.session.get('cart', {})
    q = max(0, int(request.POST.get('quantity', 1)))
    k = str(p.id)
    if q:
        c[k] = min(q, p.stock)
    else:
        c.pop(k, None)
    request.session['cart'] = c
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    c = request.session.get('cart', {})
    c.pop(str(product_id), None)
    request.session['cart'] = c
    return redirect('cart')


@login_required
def checkout(request):
    items, total = cart_data(request)
    if not items:
        return redirect('shop')
    if request.method == 'POST':
        name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        if not all([name, email, address]):
            messages.error(request, 'Complete all delivery details.')
            return render(request, 'store/checkout.html', {'items': items, 'total': total})
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=name,
                email=email,
                address=address,
                total_amount=total,
            )
            for i in items:
                p = Product.objects.select_for_update().get(id=i['product'].id)
                p.stock -= i['quantity']
                p.save()
                OrderItem.objects.create(order=order, product=p, quantity=i['quantity'], price=p.price)
        request.session['cart'] = {}
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders')
    return render(request, 'store/checkout.html', {'items': items, 'total': total})


@login_required
def orders(request):
    return render(request, 'store/orders.html', {
        'orders': Order.objects.filter(user=request.user).prefetch_related('items__product')
    })


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'store/wishlist.html', {'wishlist_items': items})


@login_required
def toggle_wishlist(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=p)
    if not created:
        item.delete()
        messages.success(request, f'{p.name} removed from your wishlist.')
    else:
        messages.success(request, f'{p.name} saved to your wishlist.')
    return redirect(request.POST.get('next') or 'wishlist')


@login_required
def add_review(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 0))
        except ValueError:
            rating = 0
        comment = request.POST.get('comment', '').strip()
        if rating not in range(1, 6):
            messages.error(request, 'Please choose a rating from 1 to 5.')
        else:
            Review.objects.update_or_create(user=request.user, product=p, defaults={'rating': rating, 'comment': comment})
            messages.success(request, 'Your review has been saved.')
    return redirect('product_detail', product_id=p.id)


@login_required
def smart_shop(request):
    raw = request.GET.get('budget', '').strip()
    budget = None
    picks = []
    if raw:
        try:
            budget = max(0, Decimal(raw))
        except Exception:
            messages.error(request, 'Enter a valid budget amount.')
    if budget is not None and budget > 0:
        # Greedy bundle: prioritize different categories, then higher-rated products, without exceeding the budget.
        qs = Product.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating','-id')
        used_categories = set()
        remaining = budget
        for product in qs:
            if product.price <= remaining and (product.category not in used_categories or len(picks) < 2):
                picks.append(product)
                used_categories.add(product.category)
                remaining -= product.price
            if len(picks) >= 4:
                break
        if len(picks) < 4:
            for product in Product.objects.order_by('price'):
                if product.id not in [x.id for x in picks] and product.price <= remaining:
                    picks.append(product)
                    remaining -= product.price
                if len(picks) >= 4:
                    break
    return render(request, 'store/smart_shop.html', {'budget': budget, 'picks': picks})

def logout_view(request):
    logout(request)
    return redirect('register')
