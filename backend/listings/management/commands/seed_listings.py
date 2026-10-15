import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from listings.models import Listing
from orders.models import Order, OrderItem
from users.models import User

DATA = {
    "Books": [
        ("Engineering Mathematics Textbook Set", 450),
        ("Data Structures in C", 320),
        ("Operating System Concepts", 380),
        ("Physics for Engineers", 290),
        ("Organic Chemistry Notes Bundle", 150),
        ("DBMS Textbook", 340),
        ("Computer Networks by Tanenbaum", 410),
        ("GATE CS Previous Papers", 200),
        ("Engineering Drawing Book", 180),
        ("Discrete Mathematics", 310),
        ("Digital Electronics Manual", 260),
        ("English Communication Workbook", 120),
        ("Thermodynamics Textbook", 350),
        ("Signals and Systems", 370),
        ("Python Programming Guide", 220),
    ],
    "Electronics": [
        ("Scientific Calculator", 650),
        ("Wireless Mouse", 400),
        ("Bluetooth Earphones", 900),
        ("Power Bank 10000mAh", 750),
        ("USB Hub 4-Port", 350),
        ("Arduino Uno Starter Kit", 1100),
        ("Laptop Cooling Pad", 600),
        ("Mechanical Keyboard", 2200),
        ("LED Desk Lamp", 450),
        ("Raspberry Pi 4 Board", 3500),
        ("Smartwatch", 1800),
        ("Portable Speaker", 1300),
        ("5-Socket Extension Board", 300),
        ("HD Webcam", 1000),
    ],
    "Hostel Essentials": [
        ("Mini Fridge", 3500),
        ("Electric Kettle", 500),
        ("Foldable Study Table", 1200),
        ("Bucket and Mug Set", 150),
        ("Single Mattress", 1800),
        ("Table Fan", 1100),
        ("Wall Mirror", 250),
        ("Storage Trunk", 900),
        ("Induction Cooktop", 1500),
        ("Clothes Drying Stand", 400),
        ("Curtain Set", 350),
        ("Room Heater", 800),
        ("Study Chair", 1300),
        ("Desk Lamp", 450),
        ("Laundry Basket", 280),
        ("Mosquito Net", 340),
    ],
    "Cycles": [
        ("Hero Sprint Cycle", 3500),
        ("Atlas Gear Cycle", 5200),
        ("Firefox Road Bike", 7500),
        ("Cycle Helmet", 600),
        ("Cycle Lock Chain", 250),
        ("Foldable Cycle", 6000),
        ("Hercules MTB", 4800),
        ("BSA Ladybird", 3000),
        ("Cycle Pump", 200),
        ("Cycle Basket Carrier", 300),
        ("Riding Gloves", 180),
        ("Cycle Light Set", 350),
        ("City Bike", 4200),
        ("Hybrid Cycle", 6100),
        ("Kids Cycle", 2600),
    ],
    "Sports": [
        ("Badminton Racket Set", 1200),
        ("Football", 900),
        ("Gym Dumbbell Pair", 1500),
        ("Yoga Mat", 500),
        ("Cricket Bat", 1100),
        ("Skipping Rope", 250),
        ("Tennis Ball Pack", 400),
        ("Volleyball", 850),
        ("Boxing Gloves", 800),
        ("Table Tennis Set", 1300),
        ("Resistance Band Kit", 700),
        ("Sports Bottle", 350),
    ],
}
CATEGORY_IMAGES = {
    "Books": [
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1541963463532-d68292c34b19?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
    ],
    "Electronics": [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=900&q=80",
    ],
    "Hostel Essentials": [
        "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1484101403633-562f891dc89a?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=900&q=80",
    ],
    "Cycles": [
        "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1558980664-10e7170b5df9?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=900&q=80",
    ],
    "Sports": [
        "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1547347298-4074fc3086f0?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=900&q=80",
    ],
}
ITEM_IMAGES = {
    "Engineering Mathematics Textbook Set": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=900&q=80",
    "Data Structures in C": "https://images.unsplash.com/photo-1524578271613-d550eacf6090?auto=format&fit=crop&w=900&q=80",
    "Operating System Concepts": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=900&q=80",
    "Physics for Engineers": "https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=900&q=80",
    "Organic Chemistry Notes Bundle": "https://images.unsplash.com/photo-1533900340604-21da7f6b5ba3?auto=format&fit=crop&w=900&q=80",
    "DBMS Textbook": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=900&q=80",
    "Computer Networks by Tanenbaum": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
    "GATE CS Previous Papers": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=900&q=80",
    "Engineering Drawing Book": "https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=900&q=80",
    "Discrete Mathematics": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
    "Digital Electronics Manual": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "English Communication Workbook": "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=900&q=80",
    "Thermodynamics Textbook": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=900&q=80",
    "Signals and Systems": "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?auto=format&fit=crop&w=900&q=80",
    "Python Programming Guide": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=900&q=80",
    "Scientific Calculator": "https://images.unsplash.com/photo-1609250291996-fde53c8f1d7a?auto=format&fit=crop&w=900&q=80",
    "Wireless Mouse": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&q=80",
    "Bluetooth Earphones": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80",
    "Power Bank 10000mAh": "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=900&q=80",
    "USB Hub 4-Port": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "Arduino Uno Starter Kit": "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?auto=format&fit=crop&w=900&q=80",
    "Laptop Cooling Pad": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
    "Mechanical Keyboard": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&q=80",
    "LED Desk Lamp": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "Raspberry Pi 4 Board": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80",
    "Smartwatch": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=900&q=80",
    "Portable Speaker": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=900&q=80",
    "5-Socket Extension Board": "https://images.unsplash.com/photo-1555618563-98c5cc0eb3eb?auto=format&fit=crop&w=900&q=80",
    "HD Webcam": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
    "Mini Fridge": "https://images.unsplash.com/photo-1585518419759-7fe2e0fbf8a6?auto=format&fit=crop&w=900&q=80",
    "Electric Kettle": "https://images.unsplash.com/photo-1563453392212-326f5e854473?auto=format&fit=crop&w=900&q=80",
    "Foldable Study Table": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "Bucket and Mug Set": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=900&q=80",
    "Single Mattress": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "Table Fan": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=80",
    "Wall Mirror": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=900&q=80",
    "Storage Trunk": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "Induction Cooktop": "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=900&q=80",
    "Clothes Drying Stand": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=900&q=80",
    "Curtain Set": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "Room Heater": "https://images.unsplash.com/photo-1556911220-dabc1f02913a?auto=format&fit=crop&w=900&q=80",
    "Study Chair": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    "Hero Sprint Cycle": "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=900&q=80",
    "Atlas Gear Cycle": "https://images.unsplash.com/photo-1558980664-10e7170b5df9?auto=format&fit=crop&w=900&q=80",
    "Firefox Road Bike": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80",
    "Cycle Helmet": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?auto=format&fit=crop&w=900&q=80",
    "Cycle Lock Chain": "https://images.unsplash.com/photo-1558980664-10e7170b5df9?auto=format&fit=crop&w=900&q=80",
    "Foldable Cycle": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=900&q=80",
    "Hercules MTB": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=900&q=80",
    "BSA Ladybird": "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=900&q=80",
    "Cycle Pump": "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=900&q=80",
    "Cycle Basket Carrier": "https://images.unsplash.com/photo-1558566018-6609f4846eb1?auto=format&fit=crop&w=900&q=80",
    "Riding Gloves": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80",
    "Cycle Light Set": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=900&q=80",
    "Badminton Racket Set": "https://images.unsplash.com/photo-1626224583764-1c0f8d50f13b?auto=format&fit=crop&w=900&q=80",
    "Football": "https://images.unsplash.com/photo-1543351611-58f69d7c1781?auto=format&fit=crop&w=900&q=80",
    "Gym Dumbbell Pair": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80",
    "Yoga Mat": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=900&q=80",
    "Cricket Bat": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=900&q=80",
    "Skipping Rope": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=900&q=80",
}
SENIOR_IDS = {9, 11, 18, 20, 42, 50}
HOSTELS = ["Hostel A", "Hostel B", "Hostel C", "Hostel D"]
CONDITIONS = ["Like New", "Good", "Fair"]


def listing_image(title, category, index):
    if title in ITEM_IMAGES:
        return ITEM_IMAGES[title]
    cat_images = CATEGORY_IMAGES.get(category, [])
    if not cat_images:
        return f"https://picsum.photos/seed/{category.lower().replace(' ', '-')}/{index}/300"
    return cat_images[index % len(cat_images)]


class Command(BaseCommand):
    help = "Seed 2 users and 54 listings (safe to run twice). --with-orders adds six finished orders."

    def add_arguments(self, parser):
        parser.add_argument("--with-orders", action="store_true")

    def handle(self, *a, with_orders=False, **kw):
        priya, _ = User.objects.get_or_create(username="Priya", defaults={"user_type": "seller", "email": "priya@campus.edu"})
        priya.set_password("secret123"); priya.user_type = "seller"; priya.save()
        arjun, _ = User.objects.get_or_create(username="Arjun", defaults={"user_type": "student", "email": "arjun@campus.edu"})
        arjun.set_password("secret123"); arjun.save()

        # round-robin the categories, then pin ids 8 and 9 to the two listings the course uses
        pools = {c: [(c, t, p) for t, p in rows] for c, rows in DATA.items()}
        items = []
        while any(pools.values()):
            for c in pools:
                if pools[c]:
                    items.append(pools[c].pop(0))
        def swap(title, idx):
            j = next(k for k, x in enumerate(items) if x[1] == title)
            items[idx], items[j] = items[j], items[idx]
        swap("Scientific Calculator", 7)
        swap("Engineering Mathematics Textbook Set", 8)

        for n, (cat, title, price) in enumerate(items, start=1):
            Listing.objects.update_or_create(id=n, defaults=dict(
                title=title, category=cat, price=price, seller=priya,
                hostel="Hostel C" if n == 9 else HOSTELS[n % 4],
                condition="Good" if n == 9 else ("Like New" if n == 8 else CONDITIONS[n % 3]),
                negotiable=n % 2 == 0 or n == 9,
                imageUrl=listing_image(title, cat, n),
                rating=4.5 if n == 9 else round(3.0 + (n * 7 % 21) / 10, 1),
                total_reviews=n * 3 % 40 + 2, availability="Available",
                description=f"{title}, used for one year by a final-year student. Collect it at a campus meetup point.",
                is_senior_deal=n in SENIOR_IDS))
        self.stdout.write(self.style.SUCCESS(f"{Listing.objects.count()} listings, users Priya and Arjun ready."))

        if with_orders and not Order.objects.exists():
            rnd = random.Random(7)
            for days_ago in (6, 5, 4, 3, 1, 0):
                o = Order.objects.create(user=arjun, payment_method="COD", meetup_point=rnd.choice(["MAIN_GATE", "LIBRARY", "CANTEEN"]),
                                         full_name="Arjun K", phone="9123456780", address="Hostel B, Room 21",
                                         city="Hyderabad", state="Telangana", pincode="500001")
                for l in Listing.objects.filter(is_senior_deal=False).order_by("?")[: rnd.randint(1, 2)]:
                    OrderItem.objects.create(order=o, listing=l, seller=priya, title=l.title, hostel=l.hostel, condition=l.condition,
                                             image_url=l.imageUrl, price=l.price, quantity=rnd.randint(1, 2), status="delivered")
                o.refresh_status()
                Order.objects.filter(pk=o.pk).update(created_at=timezone.now() - timedelta(days=days_ago))
            self.stdout.write(self.style.SUCCESS("Six delivered orders created."))
