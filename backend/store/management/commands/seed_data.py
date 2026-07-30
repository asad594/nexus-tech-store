from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Category, Product, Order, OrderItem, CartItem, Review, Wishlist

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with 5 exact authentic laptop models (Apple, Dell, HP, Lenovo, Acer) with verified laptop photos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Clearing old catalog and seeding 5 authentic laptop models...'))

        # Create Admin User
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@nexus.io',
                'name': 'Nexus Admin',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'shipping_address': 'Nexus HQ 1 Quantum Way',
                'city': 'San Jose',
                'postal_code': '95134',
                'country': 'United States',
                'avatar_url': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / admin123'))

        # Create Customer User
        customer, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'name': 'John Doe',
                'role': 'customer',
                'phone_number': '+1 (555) 234-5678',
                'shipping_address': '100 Silicon Valley Way, Suite 400',
                'city': 'San Jose',
                'postal_code': '95134',
                'country': 'United States',
                'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200',
            }
        )
        if created:
            customer.set_password('password123')
            customer.save()
            self.stdout.write(self.style.SUCCESS('Customer user created: john_doe / password123'))

        # Create Categories
        categories_data = [
            {'name': 'Laptops', 'slug': 'laptops', 'icon': 'Laptop', 'description': 'Authentic flagship laptops from Apple, Dell, HP, Lenovo, and Acer'},
            {'name': 'Phones', 'slug': 'phones', 'icon': 'Smartphone', 'description': 'Flagship foldable & holographic smartphone hardware'},
            {'name': 'Tablets', 'slug': 'tablets', 'icon': 'Tablet', 'description': 'Ultra-thin OLED digital art canvases'},
            {'name': 'Audio', 'slug': 'audio', 'icon': 'Headphones', 'description': 'Spatial lossy acoustic foam and transparent ANC buds'},
            {'name': 'Accessories', 'slug': 'accessories', 'icon': 'Watch', 'description': 'Sapphire glass wearables & Thunderbolt glass docks'},
        ]

        cat_objs = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(
                slug=cat['slug'],
                defaults={'name': cat['name'], 'icon': cat['icon'], 'description': cat['description']}
            )
            cat_objs[cat['slug']] = obj

        # Wipe old products to guarantee clean catalog without shoe pictures or outdated entries
        Product.objects.all().delete()

        # Products Seed Data: EXACTLY 5 REAL LAPTOPS (Apple, Dell, HP, Lenovo, Acer) + Curated Tech Gadgets
        products_data = [
            # --- 5 AUTHENTIC LAPTOP MODELS ---
            {
                'name': 'Apple MacBook Pro 16 M3 Max',
                'category': cat_objs['laptops'],
                'price': 3499.00,
                'brand': 'Apple',
                'description': 'Space Black Liquid Retina XDR display workstation powered by 16-core CPU M3 Max and 40-core GPU.',
                'specs': {'chip': 'Apple M3 Max', 'ram': '48GB Unified', 'storage': '1TB SSD', 'display': '16.2" Liquid Retina XDR'},
                'stock_qty': 12,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 5.0,
            },
            {
                'name': 'Dell XPS 16 OLED Titanium',
                'category': cat_objs['laptops'],
                'price': 2399.00,
                'brand': 'Dell',
                'description': 'Seamless glass palm rest with capacitive touch function row, 4K OLED touch panel, and RTX 4070 Graphics.',
                'specs': {'chip': 'Intel Core Ultra 9', 'gpu': 'RTX 4070 8GB', 'ram': '32GB LPDDR5X', 'display': '16.3" 4K OLED Touch'},
                'stock_qty': 10,
                'image_url': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'HP EliteBook 840 G10 Business',
                'category': cat_objs['laptops'],
                'price': 1599.00,
                'brand': 'HP',
                'description': 'Commercial enterprise laptop with HP Wolf Security suite, 5MP IR webcam, and spill-resistant backlit keyboard.',
                'specs': {'chip': 'Intel Core i7-1370P vPro', 'ram': '32GB DDR5', 'storage': '1TB NVMe', 'display': '14.0" WUXGA IPS 400 nits'},
                'stock_qty': 22,
                'image_url': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.8,
            },
            {
                'name': 'Lenovo ThinkPad X1 Carbon Gen 12',
                'category': cat_objs['laptops'],
                'price': 1949.00,
                'brand': 'Lenovo',
                'description': 'Legendary carbon-fiber business ultrabook featuring TrackPoint glass touchpad, 8K webcam bar, and MIL-STD 810H durability.',
                'specs': {'chip': 'Intel Core Ultra 7 165U', 'ram': '32GB LPDDR5X', 'storage': '1TB Gen4 SSD', 'display': '14.0" 2.8K OLED 120Hz'},
                'stock_qty': 20,
                'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'Acer Predator Triton 17 X',
                'category': cat_objs['laptops'],
                'price': 2999.00,
                'brand': 'Acer',
                'description': 'CNC unibody gaming titan with 5th Gen AeroBlade 3D metal fans, liquid metal thermal paste, and 250Hz Mini-LED.',
                'specs': {'chip': 'Intel i9-13900HX', 'gpu': 'RTX 4090 16GB', 'ram': '64GB DDR5', 'display': '17.0" 250Hz WQXGA Mini-LED'},
                'stock_qty': 7,
                'image_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.8,
            },

            # --- PHONES ---
            {
                'name': 'Nexus Phone 15 Ultra',
                'category': cat_objs['phones'],
                'price': 1199.00,
                'brand': 'NEXUS',
                'description': 'Titanium alloy frame with quad-sensor 200MP periscope zoom and holographic notification glyph interface.',
                'specs': {'camera': '200MP Quad Cam', 'battery': '5500mAh 100W', 'display': '6.8" 144Hz AMOLED', 'chip': 'Snapdragon 8 Gen 3'},
                'stock_qty': 30,
                'image_url': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'Aura Fold Z Neo',
                'category': cat_objs['phones'],
                'price': 1799.00,
                'brand': 'AURA',
                'description': 'Zero-gap dual foldable glass OLED panel that transforms from a sleek phone into an 8-inch high-definition canvas.',
                'specs': {'display': '8.0" Foldable Dynamic OLED', 'chip': 'Aura Bionic 5G', 'ram': '12GB RAM', 'camera': '50MP Triple OIS'},
                'stock_qty': 12,
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.7,
            },

            # --- TABLETS ---
            {
                'name': 'NexusPad Pro 13',
                'category': cat_objs['tablets'],
                'price': 1099.00,
                'brand': 'NEXUS',
                'description': 'Tandem OLED display with nano-texture glass option and active magnetic stylus support for digital artist professionals.',
                'specs': {'display': '13.0" Ultra Retina OLED', 'chip': 'Quantum M4', 'storage': '256GB SSD', 'pen': 'Stylus Pro Included'},
                'stock_qty': 18,
                'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': False,
                'rating': 4.9,
            },

            # --- AUDIO ---
            {
                'name': 'Nexus SoundPods Max',
                'category': cat_objs['audio'],
                'price': 449.00,
                'brand': 'NEXUS',
                'description': 'Over-ear spatial audio headphones with acoustic memory foam cushions and active hybrid ANC up to -45dB.',
                'specs': {'anc': 'Hybrid Active Noise Cancelling', 'battery': '45h Playtime', 'drivers': '40mm Titanium', 'codec': 'LDAC Lossless'},
                'stock_qty': 35,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },

            # --- ACCESSORIES ---
            {
                'name': 'Nexus Watch Ultra Glass',
                'category': cat_objs['accessories'],
                'price': 699.00,
                'brand': 'NEXUS',
                'description': 'Sapphire glass screen with aerospace titanium case, dual-frequency GPS, and 100m water resistance rating.',
                'specs': {'display': '2.0" Sapphire OLED 3000 nits', 'battery': '72h Extreme Mode', 'sensors': 'ECG, SpO2, Temp', 'water': '100m WR'},
                'stock_qty': 22,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': False,
                'rating': 4.8,
            },
        ]

        product_instances = []
        for p_data in products_data:
            p = Product.objects.create(**p_data)
            product_instances.append(p)

        laptops_count = Product.objects.filter(category=cat_objs['laptops']).count()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded catalog! Total Laptops: {laptops_count} (Apple, Dell, HP, Lenovo, Acer), Total Products: {len(product_instances)}.'))

        # Create Sample Reviews for Laptops
        for p in product_instances[:5]:
            Review.objects.create(
                product=p,
                user=customer,
                rating=5,
                comment=f"Exceptional hardware performance and sleek design for {p.name}!"
            )
