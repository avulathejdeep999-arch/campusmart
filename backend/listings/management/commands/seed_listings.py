import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from listings.models import Listing
from orders.models import Order, OrderItem
from users.models import User

DATA = {
    "Books": [("Engineering Mathematics Textbook Set", 450), ("Data Structures in C", 320), ("Operating System Concepts", 380),
              ("Physics for Engineers", 290), ("Organic Chemistry Notes Bundle", 150), ("DBMS Textbook", 340),
              ("Computer Networks by Tanenbaum", 410), ("GATE CS Previous Papers", 200), ("Engineering Drawing Book", 180),
              ("Discrete Mathematics", 310), ("Digital Electronics Manual", 260), ("English Communication Workbook", 120),
              ("Thermodynamics Textbook", 350), ("Signals and Systems", 370), ("Python Programming Guide", 220)],
    "Electronics": [("Scientific Calculator", 650), ("Wireless Mouse", 400), ("Bluetooth Earphones", 900), ("Power Bank 10000mAh", 750),
                    ("USB Hub 4-Port", 350), ("Arduino Uno Starter Kit", 1100), ("Laptop Cooling Pad", 600), ("Mechanical Keyboard", 2200),
                    ("LED Desk Lamp", 450), ("Raspberry Pi 4 Board", 3500), ("Smartwatch", 1800), ("Portable Speaker", 1300),
                    ("5-Socket Extension Board", 300), ("HD Webcam", 1000)],
    "Hostel Essentials": [("Mini Fridge", 3500), ("Electric Kettle", 500), ("Foldable Study Table", 1200), ("Bucket and Mug Set", 150),
                          ("Single Mattress", 1800), ("Table Fan", 1100), ("Wall Mirror", 250), ("Storage Trunk", 900),
                          ("Induction Cooktop", 1500), ("Clothes Drying Stand", 400), ("Curtain Set", 350), ("Room Heater", 800),
                          ("Study Chair", 1300)],
    "Cycles": [("Hero Sprint Cycle", 3500), ("Atlas Gear Cycle", 5200), ("Firefox Road Bike", 7500), ("Cycle Helmet", 600),
               ("Cycle Lock Chain", 250), ("Foldable Cycle", 6000), ("Hercules MTB", 4800), ("BSA Ladybird", 3000),
               ("Cycle Pump", 200), ("Cycle Basket Carrier", 300), ("Riding Gloves", 180), ("Cycle Light Set", 350)],
}
SENIOR_IDS = {9, 11, 18, 20, 42, 50}
HOSTELS = ["Hostel A", "Hostel B", "Hostel C", "Hostel D"]
CONDITIONS = ["Like New", "Good", "Fair"]


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
                imageUrl=f"https://picsum.photos/seed/listing{n}/300/300",
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
