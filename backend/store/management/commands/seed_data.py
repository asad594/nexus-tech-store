from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Category, Product, Order, OrderItem, CartItem, Review, Wishlist

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with realistic dummy electronics data matching the NEXUS futuristic UI'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Seeding database with 30 Laptop items (Apple, Dell, HP, Lenovo, Acer) with 100% unique image URLs...'))

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
            {'name': 'Laptops', 'slug': 'laptops', 'icon': 'Laptop', 'description': 'Futuristic workstations & ultrabooks from Apple, Dell, HP, Lenovo & Acer'},
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

        # Clean existing laptops to ensure exact 30 items without duplicates
        Product.objects.filter(category=cat_objs['laptops']).delete()

        # Products Seed Data: 30 LAPTOPS ONLY FROM Apple, Dell, HP, Lenovo & Acer with 100% Unique Image URLs
        products_data = [
            # --- APPLE MACBOOK (6 Models) ---
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
                'name': 'Apple MacBook Air 15 M3',
                'category': cat_objs['laptops'],
                'price': 1299.00,
                'brand': 'Apple',
                'description': 'Impossibly thin 15-inch aluminum design with fanless M3 efficiency and MagSafe 3 charging.',
                'specs': {'chip': 'Apple M3 8-Core', 'ram': '16GB Unified', 'storage': '512GB SSD', 'display': '15.3" Liquid Retina'},
                'stock_qty': 30,
                'image_url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'Apple MacBook Pro 14 M3 Pro',
                'category': cat_objs['laptops'],
                'price': 1999.00,
                'brand': 'Apple',
                'description': 'Compact power titan for creative professionals with 18-hour battery and 120Hz ProMotion display.',
                'specs': {'chip': 'Apple M3 Pro', 'ram': '18GB Unified', 'storage': '512GB SSD', 'display': '14.2" ProMotion 120Hz'},
                'stock_qty': 20,
                'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.8,
            },
            {
                'name': 'Apple MacBook Air 13 M2',
                'category': cat_objs['laptops'],
                'price': 1099.00,
                'brand': 'Apple',
                'description': 'Midnight blue unibody design with silent fanless cooling and 500-nit Liquid Retina display.',
                'specs': {'chip': 'Apple M2 8-Core', 'ram': '16GB Unified', 'storage': '256GB SSD', 'display': '13.6" Liquid Retina'},
                'stock_qty': 25,
                'image_url': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.8,
            },
            {
                'name': 'Apple MacBook Pro 16 M2 Max Space Gray',
                'category': cat_objs['laptops'],
                'price': 2999.00,
                'brand': 'Apple',
                'description': 'Flagship M2 Max architecture with HDMI 2.1 8K output and SDXC card reader.',
                'specs': {'chip': 'Apple M2 Max', 'ram': '32GB Unified', 'storage': '1TB SSD', 'display': '16.2" Liquid Retina XDR'},
                'stock_qty': 15,
                'image_url': 'https://images.unsplash.com/photo-1537498425277-c283d32ef9db?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.9,
            },
            {
                'name': 'Apple MacBook Air 13 Retina Gold',
                'category': cat_objs['laptops'],
                'price': 999.00,
                'brand': 'Apple',
                'description': 'Ultra-portable golden finish chassis with Touch ID glass sensor and dual Thunderbolt ports.',
                'specs': {'chip': 'Apple M1 8-Core', 'ram': '8GB Unified', 'storage': '256GB SSD', 'display': '13.3" Retina Display'},
                'stock_qty': 18,
                'image_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.7,
            },

            # --- DELL (6 Models) ---
            {
                'name': 'Dell XPS 16 OLED Platinum',
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
                'name': 'Dell Alienware m18 R2 Gaming',
                'category': cat_objs['laptops'],
                'price': 3199.00,
                'brand': 'Dell',
                'description': '18-inch desktop replacement beast featuring Element 31 thermal liquid metal and Cherry MX mechanical keycaps.',
                'specs': {'chip': 'Intel i9-14900HX', 'gpu': 'RTX 4090 16GB', 'ram': '64GB DDR5', 'display': '18.0" 480Hz FHD+'},
                'stock_qty': 6,
                'image_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'Dell XPS 14 Compact Glass',
                'category': cat_objs['laptops'],
                'price': 1699.00,
                'brand': 'Dell',
                'description': 'CNC machined aluminum chassis with Gorilla Glass 3 borderless display and AI-accelerated NPU processor.',
                'specs': {'chip': 'Intel Core Ultra 7', 'gpu': 'RTX 4050 6GB', 'ram': '16GB LPDDR5X', 'display': '14.5" 3.2K OLED'},
                'stock_qty': 18,
                'image_url': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.6,
            },
            {
                'name': 'Dell Latitude 9450 2-in-1',
                'category': cat_objs['laptops'],
                'price': 2099.00,
                'brand': 'Dell',
                'description': 'Enterprise convertible 2-in-1 featuring haptic collaboration touchpad and zero-lattice zero-energy keyboard.',
                'specs': {'chip': 'Intel Core Ultra 7 vPro', 'ram': '32GB LPDDR5x', 'storage': '1TB SSD', 'display': '14.0" QHD+ Touch 360°'},
                'stock_qty': 14,
                'image_url': 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.7,
            },
            {
                'name': 'Dell Inspiron 16 Plus OLED',
                'category': cat_objs['laptops'],
                'price': 1349.00,
                'brand': 'Dell',
                'description': 'Ice Blue aluminum finish with ComfortView Plus low blue light screen and ExpressCharge battery technology.',
                'specs': {'chip': 'Intel Core Ultra 7 155H', 'gpu': 'RTX 4060 8GB', 'ram': '16GB LPDDR5X', 'display': '16.0" 2.5K 120Hz'},
                'stock_qty': 20,
                'image_url': 'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.6,
            },
            {
                'name': 'Dell Alienware x16 R2 Slim',
                'category': cat_objs['laptops'],
                'price': 2799.00,
                'brand': 'Dell',
                'description': 'Ultra-thin 18.5mm Lunar Light chassis with 100-micro LED rear stadium lighting strip and Cryo-Tech cooling.',
                'specs': {'chip': 'Intel Core Ultra 9 185H', 'gpu': 'RTX 4080 12GB', 'ram': '32GB LPDDR5X', 'display': '16.0" 240Hz QHD+'},
                'stock_qty': 9,
                'image_url': 'https://images.unsplash.com/photo-1542393545-10f5cde2c810?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.8,
            },

            # --- HP (6 Models) ---
            {
                'name': 'HP EliteBook 840 G10 Business',
                'category': cat_objs['laptops'],
                'price': 1599.00,
                'brand': 'HP',
                'description': 'Commercial enterprise laptop with HP Wolf Security suite, 5MP IR webcam, and spill-resistant backlit keyboard.',
                'specs': {'chip': 'Intel Core i7-1370P vPro', 'ram': '32GB DDR5', 'storage': '1TB NVMe', 'display': '14.0" WUXGA IPS 400 nits'},
                'stock_qty': 22,
                'image_url': 'https://images.unsplash.com/photo-1585060544812-6b45742d762f?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'HP Spectre x360 16 OLED',
                'category': cat_objs['laptops'],
                'price': 1899.00,
                'brand': 'HP',
                'description': 'Gem-cut 360-degree convertible with 9MP AI auto-frame webcam and quad Bang & Olufsen tuned acoustic speakers.',
                'specs': {'chip': 'Intel Core Ultra 7 155H', 'ram': '32GB LPDDR5', 'storage': '2TB NVMe', 'display': '16.0" 2.8K OLED Touch'},
                'stock_qty': 15,
                'image_url': 'https://images.unsplash.com/photo-1544731612-de7f96afe55f?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.8,
            },
            {
                'name': 'HP OMEN Transcend 14',
                'category': cat_objs['laptops'],
                'price': 1599.00,
                'brand': 'HP',
                'description': 'The world\'s lightest 14-inch gaming laptop with IMAX Enhanced OLED screen and HyperX wireless headset pairing.',
                'specs': {'chip': 'Intel Core Ultra 9 185H', 'gpu': 'RTX 4070 8GB', 'ram': '32GB LPDDR5X', 'display': '14.0" 2.8K 120Hz OLED'},
                'stock_qty': 22,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.7,
            },
            {
                'name': 'HP Dragonfly Pro Studio',
                'category': cat_objs['laptops'],
                'price': 1749.00,
                'brand': 'HP',
                'description': 'Ultra-premium business laptop with 400-nit high brightness display, 24/7 concierge support integration, and sustainable recycled alloys.',
                'specs': {'chip': 'AMD Ryzen 7 PRO 7736U', 'ram': '32GB LPDDR5', 'storage': '1TB SSD', 'display': '14.0" 120Hz Touch'},
                'stock_qty': 11,
                'image_url': 'https://images.unsplash.com/photo-1587614382346-4ec70e388b28?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.6,
            },
            {
                'name': 'HP ZBook Studio G10 Workstation',
                'category': cat_objs['laptops'],
                'price': 2699.00,
                'brand': 'HP',
                'description': 'Heavyweight mobile workstation engineered for 8K rendering, CAD modelling, and ISV software certification.',
                'specs': {'chip': 'Intel Core i9-13900H', 'gpu': 'NVIDIA RTX 4000 Ada', 'ram': '64GB DDR5', 'display': '16.0" DreamColor 120Hz'},
                'stock_qty': 7,
                'image_url': 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.9,
            },
            {
                'name': 'HP Envy x360 15 Convertible',
                'category': cat_objs['laptops'],
                'price': 1199.00,
                'brand': 'HP',
                'description': 'Natural silver aluminum 360-degree convertible with HP Rechargeable Tilt Pen and manual camera shutter.',
                'specs': {'chip': 'AMD Ryzen 7 7730U', 'ram': '16GB LPDDR4x', 'storage': '1TB SSD', 'display': '15.6" FHD IPS Touch'},
                'stock_qty': 25,
                'image_url': 'https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.6,
            },

            # --- LENOVO (6 Models) ---
            {
                'name': 'Lenovo ThinkPad X1 Carbon Gen 12',
                'category': cat_objs['laptops'],
                'price': 1949.00,
                'brand': 'Lenovo',
                'description': 'Legendary carbon-fiber business ultrabook featuring TrackPoint glass touchpad, 8K webcam bar, and MIL-STD 810H durability.',
                'specs': {'chip': 'Intel Core Ultra 7 165U', 'ram': '32GB LPDDR5X', 'storage': '1TB Gen4 SSD', 'display': '14.0" 2.8K OLED 120Hz'},
                'stock_qty': 20,
                'image_url': 'https://images.unsplash.com/photo-1516387080803-5188d8b9d36a?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.9,
            },
            {
                'name': 'Lenovo Legion Pro 7i Gen 9',
                'category': cat_objs['laptops'],
                'price': 2599.00,
                'brand': 'Lenovo',
                'description': 'AI-tuned gaming powerhouse with LA2-Q AI chip, Coldfront 5.0 vapor chamber, and TrueStrike RGB keyboard.',
                'specs': {'chip': 'Intel i9-14900HX', 'gpu': 'RTX 4080 12GB', 'ram': '32GB DDR5', 'display': '16.0" 240Hz WQXGA'},
                'stock_qty': 12,
                'image_url': 'https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.8,
            },
            {
                'name': 'Lenovo Yoga Book 9i Dual Screen',
                'category': cat_objs['laptops'],
                'price': 1999.00,
                'brand': 'Lenovo',
                'description': 'Revolutionary dual 13.3-inch OLED touchscreen laptop with origami stand, bluetooth detachable keyboard, and stylus pen.',
                'specs': {'chip': 'Intel Core Ultra 7', 'ram': '16GB LPDDR5X', 'storage': '1TB SSD', 'display': 'Dual 13.3" 2.8K OLED Touch'},
                'stock_qty': 9,
                'image_url': 'https://images.unsplash.com/photo-1522199755839-a2bacb67c546?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': False,
                'rating': 4.7,
            },
            {
                'name': 'Lenovo ThinkPad P1 Gen 6 Workstation',
                'category': cat_objs['laptops'],
                'price': 2899.00,
                'brand': 'Lenovo',
                'description': 'Slim 16-inch mobile workstation with liquid metal thermal cooling and factory color-calibrated OLED display.',
                'specs': {'chip': 'Intel Core i9-13900H', 'gpu': 'NVIDIA RTX 3500 Ada', 'ram': '64GB DDR5', 'display': '16.0" 4K OLED Touch'},
                'stock_qty': 8,
                'image_url': 'https://images.unsplash.com/photo-1530893609608-32a9af3aa95c?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.9,
            },
            {
                'name': 'Lenovo Slim 7i Aura Edition',
                'category': cat_objs['laptops'],
                'price': 1279.00,
                'brand': 'Lenovo',
                'description': 'Sleek dark lunar gray metal chassis with smart share tap-to-transfer tech and ultra-low power consumption.',
                'specs': {'chip': 'Intel Core Ultra 7 258V', 'ram': '32GB LPDDR5X', 'storage': '1TB SSD', 'display': '15.3" 2.8K 120Hz'},
                'stock_qty': 25,
                'image_url': 'https://images.unsplash.com/photo-1504707748692-419802cf939d?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.6,
            },
            {
                'name': 'Lenovo IdeaPad Pro 5i OLED',
                'category': cat_objs['laptops'],
                'price': 1099.00,
                'brand': 'Lenovo',
                'description': 'Arctic Grey all-metal chassis with 120Hz OLED screen and 84Whr battery for all-day creative workflows.',
                'specs': {'chip': 'Intel Core Ultra 5 125H', 'ram': '16GB LPDDR5x', 'storage': '512GB SSD', 'display': '14.0" 2.8K 120Hz OLED'},
                'stock_qty': 28,
                'image_url': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.6,
            },

            # --- ACER (6 Models) ---
            {
                'name': 'Acer Predator Triton 17 X',
                'category': cat_objs['laptops'],
                'price': 2999.00,
                'brand': 'Acer',
                'description': 'CNC unibody gaming titan with 5th Gen AeroBlade 3D metal fans, liquid metal thermal paste, and 250Hz Mini-LED.',
                'specs': {'chip': 'Intel i9-13900HX', 'gpu': 'RTX 4090 16GB', 'ram': '64GB DDR5', 'display': '17.0" 250Hz WQXGA Mini-LED'},
                'stock_qty': 7,
                'image_url': 'https://images.unsplash.com/photo-1511556532299-8f662fc26c06?q=80&w=1000&auto=format&fit=crop',
                'is_featured': True,
                'is_new': True,
                'rating': 4.8,
            },
            {
                'name': 'Acer Swift 14 AI OLED Ultrabook',
                'category': cat_objs['laptops'],
                'price': 1199.00,
                'brand': 'Acer',
                'description': 'Copilot+ PC featuring Qualcomm Snapdragon X Elite neural processing and iridescent multi-color LED trackpad indicator.',
                'specs': {'chip': 'Snapdragon X Elite 12-Core', 'ram': '16GB LPDDR5X', 'storage': '1TB SSD', 'display': '14.5" 2.8K 120Hz OLED'},
                'stock_qty': 28,
                'image_url': 'https://images.unsplash.com/photo-1563770660941-20978e870e26?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.6,
            },
            {
                'name': 'Acer Nitro 16 Gaming Laptop',
                'category': cat_objs['laptops'],
                'price': 1249.00,
                'brand': 'Acer',
                'description': 'Obsidian Black chassis with 4-zone RGB backlit keyboard, dual-fan cooling with liquid metal, and MUX switch.',
                'specs': {'chip': 'AMD Ryzen 7 7840HS', 'gpu': 'RTX 4060 8GB', 'ram': '16GB DDR5', 'display': '16.0" 165Hz WQXGA'},
                'stock_qty': 22,
                'image_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.7,
            },
            {
                'name': 'Acer Swift Go 16 OLED Touch',
                'category': cat_objs['laptops'],
                'price': 999.00,
                'brand': 'Acer',
                'description': 'Thin & light aluminum ultrabook featuring 3.2K OLED panel with 100% DCI-P3 color gamut and 1440p QHD webcam.',
                'specs': {'chip': 'Intel Core Ultra 7 155H', 'ram': '16GB LPDDR5x', 'storage': '1TB SSD', 'display': '16.0" 3.2K 120Hz OLED'},
                'stock_qty': 25,
                'image_url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.6,
            },
            {
                'name': 'Acer Predator Helios 18',
                'category': cat_objs['laptops'],
                'price': 2499.00,
                'brand': 'Acer',
                'description': 'High-performance desktop replacement with per-key RGB MagKey 3.0 mechanical switches and MagClick tactile feedback.',
                'specs': {'chip': 'Intel i9-14900HX', 'gpu': 'RTX 4080 12GB', 'ram': '32GB DDR5', 'display': '18.0" 250Hz Mini-LED'},
                'stock_qty': 10,
                'image_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': True,
                'rating': 4.8,
            },
            {
                'name': 'Acer Chromebook Plus 515',
                'category': cat_objs['laptops'],
                'price': 499.00,
                'brand': 'Acer',
                'description': 'Fast Google AI-powered Chromebook featuring 1080p webcam with temporal noise reduction and fast charging.',
                'specs': {'chip': 'Intel Core i5-1335U', 'ram': '8GB LPDDR5', 'storage': '256GB UFS', 'display': '15.6" Full HD IPS'},
                'stock_qty': 35,
                'image_url': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?q=80&w=1000&auto=format&fit=crop',
                'is_featured': False,
                'is_new': False,
                'rating': 4.5,
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

        laptops_count = Product.objects.filter(category=cat_objs['laptops']).count()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded catalog! Total Laptops: {laptops_count} (Apple, Dell, HP, Lenovo, Acer), Total Products: {len(product_instances)}.'))

        # Create Sample Reviews
        sample_reviews = [
            (product_instances[0], customer, 5, "Unbelievable build quality and speed! The Liquid Glass trackpad feels incredible."),
            (product_instances[0], admin, 5, "Our flagship workstation. Absolute perfection for developer multitasking."),
            (product_instances[6], customer, 5, "The 4K OLED touch display on this Dell XPS 16 is astonishing."),
            (product_instances[12], customer, 5, "HP EliteBook build quality and Wolf Security features are top tier."),
            (product_instances[18], customer, 5, "ThinkPad X1 Carbon keyboard and 2.8K OLED screen remain unmatched."),
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
                product=product_instances[6],
                product_name_snapshot=product_instances[6].name,
                quantity=1,
                price_at_purchase=product_instances[6].price
            )
            self.stdout.write(self.style.SUCCESS('Sample order created for john_doe.'))
