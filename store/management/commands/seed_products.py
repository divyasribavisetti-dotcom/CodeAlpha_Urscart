from django.core.management.base import BaseCommand
from store.models import Product

# Real product photography from Unsplash. Keep these as direct image URLs (not Markdown links).
DATA = [
('Aurora Wireless Headphones','Immersive wireless headphones with clear audio and long battery life.',2499,18,'Tech & Gadgets','https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1000&q=88'),
('Minimal Smart Watch','A sleek smartwatch for activity tracking and daily notifications.',3299,14,'Tech & Gadgets','https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1000&q=88'),
('Pocket Bluetooth Speaker','Compact sound with a rich everyday listening experience.',1799,16,'Tech & Gadgets','https://images.unsplash.com/photo-1608043152269-423dbba4e7c1?auto=format&fit=crop&w=1000&q=88'),
('Canvas Backpack','A lightweight backpack for college, work and travel.',1599,22,'Fashion','https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=88'),
('Urban Running Sneakers','Comfortable everyday sneakers with modern athletic styling.',2899,20,'Fashion','https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1000&q=88'),
('Linen Everyday Tote','A clean, roomy tote for campus, work and weekend plans.',1199,24,'Fashion','https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=1000&q=88'),
('Ceramic Coffee Set','A refined cup and saucer set for a calm cafe feel at home.',899,30,'Home & Living','https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=1000&q=88'),
('Modern Desk Lamp','Warm adjustable lighting for study, coding and cozy evenings.',1299,16,'Home & Living','https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1000&q=88'),
('Scented Candle Set','Soft fragrance and a warm glow for relaxed evenings.',749,26,'Home & Living','https://images.unsplash.com/photo-1603006905003-be475563bc59?auto=format&fit=crop&w=1000&q=88'),
('Glow Skincare Kit','A simple daily care set designed for a fresh routine.',1499,18,'Beauty & Care','https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=1000&q=88'),
('Velvet Lip Care','Hydrating everyday lip care with a soft finish.',599,28,'Beauty & Care','https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=1000&q=88'),
('Daily Planner Notebook','A premium planner for goals, study schedules and notes.',499,40,'Stationery','https://images.unsplash.com/photo-1531346680769-a1d79b57de5b?auto=format&fit=crop&w=1000&q=88'),
('Studio Gel Pens','Smooth-writing pens for notes, journaling and creative work.',299,45,'Stationery','https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1000&q=88'),
('Pastel Sticky Notes','Colorful sticky notes for reminders, ideas and study sessions.',199,50,'Stationery','https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?auto=format&fit=crop&w=1000&q=88'),
('Balance Yoga Mat','A comfortable non-slip mat for stretching and everyday workouts.',1199,18,'Sports & Fitness','https://images.unsplash.com/photo-1592432678016-e910b452f9a2?auto=format&fit=crop&w=1000&q=88'),
('Hydra Fitness Bottle','Double-wall insulated bottle for workouts and everyday use.',699,35,'Sports & Fitness','https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1000&q=88'),
('Travel Organizer','Keep chargers, documents and little essentials neatly together.',899,25,'Travel','https://images.unsplash.com/photo-1553531384-397c80973a0b?auto=format&fit=crop&w=1000&q=88'),
('Weekend Duffle','A versatile carry-all for short trips and weekend plans.',1999,14,'Travel','https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=88'),
('Focus Study Lamp','A focused desk light for late-night study and project work.',1399,17,'Study Essentials','https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?auto=format&fit=crop&w=1000&q=88'),
('Planner Sticker Pack','A playful set of stickers for planners, notes and study boards.',249,42,'Study Essentials','https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=1000&q=88'),
]

class Command(BaseCommand):
    help = 'Seed Urs Cart products with direct product photography URLs.'

    def handle(self, *args, **kwargs):
        for n, d, pr, s, c, img in DATA:
            Product.objects.update_or_create(
                name=n,
                defaults={'description': d, 'price': pr, 'stock': s, 'category': c, 'image_url': img}
            )
        self.stdout.write(self.style.SUCCESS(f'Urs Cart products ready: {len(DATA)} products.'))
