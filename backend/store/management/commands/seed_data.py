from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Category, Product, Order, OrderItem, CartItem, Review, Wishlist

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with realistic dummy electronics data matching the NEXUS futuristic UI'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding database...'))

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
            {'name': 'Laptops', 'slug': 'laptops', 'icon': 'Laptop', 'description': 'Futuristic workstations & quantum ultrabooks'},
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

        # Products Seed Data
        products_data = [
            # Laptops
            {
                'name': 'NexusBook Pro X16',
                'category': cat_objs['laptops'],
                'price': 2499.00,
                'brand': 'NEXUS',
                'description': 'The ultimate futuristic workstation with liquid glass trackpad, Quantum OLED display, and M3 Max architecture.',
                'specs': {'chip': 'Quantum M3 Max', 'ram': '36GB Unified', 'storage': '1TB NVMe Gen4', 'display': '16.2" 120Hz Mini-LED'},
                'stock_qty': 15,
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'Aura Air 14 Glass',
                'category': cat_objs['laptops'],
                'price': 1399.00,
                'brand': 'AURA',
                'description': 'Ultra-thin aerospace aluminum body with silent fanless cooling and all-day 22-hour battery life.',
                'specs': {'chip': 'Aura Silicon 2', 'ram': '16GB RAM', 'storage': '512GB SSD', 'weight': '1.24 kg'},
                'stock_qty': 25,
                'image_url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': False,
                'rating': 4.8,
            },
            {
                'name': 'Cyberware Blade 15',
                'category': cat_objs['laptops'],
                'price': 2899.00,
                'brand': 'CYBERWARE',
                'description': 'Next-gen raytracing gaming titan with RTX 4090 Mobile, per-key RGB glass keyboard, and vapor chamber cooling.',
                'specs': {'chip': 'Intel i9-14900HX', 'gpu': 'RTX 4090 16GB', 'ram': '32GB DDR5', 'display': '240Hz QHD+'},
                'stock_qty': 8,
                'image_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.9,
            },
            # Phones
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
            {
                'name': 'Vortex Phone One',
                'category': cat_objs['phones'],
                'price': 799.00,
                'brand': 'VORTEX',
                'description': 'Clean minimalist transparent glass back panel with ambient LED pulse indicators and stock Android OS.',
                'specs': {'chip': 'MediaTek Dimensity 9200+', 'camera': '50MP Dual Sony', 'battery': '5000mAh 67W', 'display': '6.67" 120Hz OLED'},
                'stock_qty': 20,
                'image_url': 'https://images.unsplash.com/photo-1580910051074-3eb694886505?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.6,
            },
            # Tablets
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
            {
                'name': 'Aura Tab Lite 11',
                'category': cat_objs['tablets'],
                'price': 499.00,
                'brand': 'AURA',
                'description': 'Lightweight metal unibody media tablet with quad Dolby Atmos speakers and eye-care TÜV certified screen.',
                'specs': {'display': '11.0" 2K 120Hz', 'chip': 'Octa-Core 2.8GHz', 'audio': 'Quad Dolby Atmos', 'battery': '8000mAh'},
                'stock_qty': 40,
                'image_url': 'https://images.unsplash.com/photo-1561154464-82e9adf32764?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.5,
            },
            # Audio
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
            {
                'name': 'Aura Buds Pulse',
                'category': cat_objs['audio'],
                'price': 199.00,
                'brand': 'AURA',
                'description': 'Transparent glass charging case with stem touch controls, spatial audio tracking, and IPX5 water resistance.',
                'specs': {'anc': 'Adaptive ANC 2.0', 'battery': '8h + 24h Case', 'mic': 'Triple AI Beamforming', 'waterproof': 'IPX5'},
                'stock_qty': 50,
                'image_url': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.7,
            },
            # Accessories
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
            {
                'name': 'CyberDock 12-in-1 Glass Station',
                'category': cat_objs['accessories'],
                'price': 229.00,
                'brand': 'CYBERWARE',
                'description': 'RGB illuminated transparent glass Thunderbolt 4 dock with dual 4K 120Hz output and 100W PD charging.',
                'specs': {'ports': '12 Ports Dual HDMI/DP', 'speed': '40Gbps Thunderbolt 4', 'power': '100W Pass-Through', 'rgb': 'Custom RGB Glow'},
                'stock_qty': 14,
                'image_url': 'https://images.unsplash.com/photo-1625772452859-1c03d5bf1137?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.6,
            },
        ]

        product_instances = []
        for p_data in products_data:
            p, _ = Product.objects.update_or_create(
                name=p_data['name'],
                defaults=p_data
            )
            product_instances.append(p)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(product_instances)} electronic products!'))

        # Create Sample Reviews
        sample_reviews = [
            (product_instances[0], customer, 5, "Unbelievable build quality and speed! The Liquid Glass trackpad feels incredible."),
            (product_instances[0], admin, 5, "Our flagship workstation. Absolute perfection for developer multitasking."),
            (product_instances[3], customer, 5, "The 200MP camera zoom captures staggering details at night."),
            (product_instances[8], customer, 5, "Spatial audio quality is out of this world. Soundstage is so wide."),
        ]
        for prod, usr, rat, comm in sample_reviews:
            Review.objects.update_or_create(
                product=prod, user=usr,
                defaults={'rating': rat, 'comment': comm}
            )

        # Create Sample Order
        if not Order.objects.filter(user=customer).exists():
            order = Order.objects.create(
                user=customer,
                status='delivered',
                payment_status='paid',
                total_amount=3698.00,
                shipping_cost=0.00,
                shipping_address='100 Silicon Valley Way, Suite 400',
                city='San Jose',
                postal_code='95134',
                country='United States',
                payment_method='Credit Card',
                tracking_number='NEXUS-TRACK-99481A'
            )
            OrderItem.objects.create(
                order=order,
                product=product_instances[0],
                product_name_snapshot=product_instances[0].name,
                quantity=1,
                price_at_purchase=product_instances[0].price
            )
            OrderItem.objects.create(
                order=order,
                product=product_instances[3],
                product_name_snapshot=product_instances[3].name,
                quantity=1,
                price_at_purchase=product_instances[3].price
            )
            self.stdout.write(self.style.SUCCESS('Sample order created for john_doe.'))
