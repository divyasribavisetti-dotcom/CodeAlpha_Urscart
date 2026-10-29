from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name=models.CharField(max_length=150)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image_url=models.URLField(blank=True)
    stock=models.PositiveIntegerField(default=10)
    category=models.CharField(max_length=80,default='Featured')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Order(models.Model):
    STATUS_CHOICES=[('Placed','Placed'),('Processing','Processing'),('Shipped','Shipped'),('Delivered','Delivered')]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    full_name=models.CharField(max_length=150)
    email=models.EmailField()
    address=models.TextField()
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Placed')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Order #{self.id}'

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist_items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='wishlisted_by')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','product'],name='unique_user_product_wishlist')]
    def __str__(self): return f'{self.user.username} · {self.product.name}'

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='product_reviews')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveSmallIntegerField()
    comment=models.TextField(blank=True,max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['user','product'],name='unique_user_product_review')]
        ordering=['-created_at']
    def __str__(self): return f'{self.product.name} · {self.rating}/5'
