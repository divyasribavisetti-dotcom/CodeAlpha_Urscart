from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Product', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=150)),('description', models.TextField()),
            ('price', models.DecimalField(decimal_places=2, max_digits=10)),('image_url', models.URLField(blank=True)),
            ('stock', models.PositiveIntegerField(default=10)),('category', models.CharField(default='Featured', max_length=80)),
            ('created_at', models.DateTimeField(auto_now_add=True)),]),
        migrations.CreateModel(name='Order', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('full_name', models.CharField(max_length=150)),('email', models.EmailField(max_length=254)),('address', models.TextField()),
            ('total_amount', models.DecimalField(decimal_places=2,max_digits=10)),('status',models.CharField(choices=[('Placed','Placed'),('Processing','Processing'),('Shipped','Shipped'),('Delivered','Delivered')],default='Placed',max_length=20)),('created_at',models.DateTimeField(auto_now_add=True)),
            ('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='orders',to=settings.AUTH_USER_MODEL)),]),
        migrations.CreateModel(name='OrderItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('quantity',models.PositiveIntegerField()),('price',models.DecimalField(decimal_places=2,max_digits=10)),
            ('order',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='items',to='store.order')),
            ('product',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to='store.product')),]),
        migrations.CreateModel(name='Wishlist', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('created_at',models.DateTimeField(auto_now_add=True)),
            ('product',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='wishlisted_by',to='store.product')),
            ('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='wishlist_items',to=settings.AUTH_USER_MODEL)),]),
        migrations.CreateModel(name='Review', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('rating',models.PositiveSmallIntegerField()),('comment',models.TextField(blank=True,max_length=500)),('created_at',models.DateTimeField(auto_now_add=True)),
            ('product',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='reviews',to='store.product')),
            ('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='product_reviews',to=settings.AUTH_USER_MODEL)),]),
        migrations.AddConstraint(model_name='wishlist', constraint=models.UniqueConstraint(fields=('user','product'),name='unique_user_product_wishlist')),
        migrations.AddConstraint(model_name='review', constraint=models.UniqueConstraint(fields=('user','product'),name='unique_user_product_review')),
    ]
