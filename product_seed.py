from MyApp.models import Product, Category

def run():
    products_seed_data = [
        {
            "pname": "Wireless Mouse",
            "pprice": 599,
            "pdis": "Ergonomic wireless mouse with smooth tracking and long battery life.",
            "pimage": "product/mouse.jpg",
            "c_id": 1
        },
        {
            "pname": "Mechanical Keyboard",
            "pprice": 2499,
            "pdis": "RGB mechanical keyboard with blue switches for fast typing and gaming.",
            "pimage": "product/keyboard.jpg",
            "c_id": 1
        },
        {
            "pname": "Bluetooth Speaker",
            "pprice": 1299,
            "pdis": "Portable Bluetooth speaker with deep bass and 10 hours playback.",
            "pimage": "product/speaker.jpg",
            "c_id": 2
        },
        {
            "pname": "Smart Watch",
            "pprice": 1999,
            "pdis": "Fitness smartwatch with heart rate monitor and step tracking.",
            "pimage": "product/smartwatch.jpg",
            "c_id": 2
        },
        {
            "pname": "Gaming Headphones",
            "pprice": 1499,
            "pdis": "Over-ear gaming headphones with noise cancellation and mic support.",
            "pimage": "product/headphones.jpg",
            "c_id": 1
        },
        {
            "pname": "Laptop Stand",
            "pprice": 799,
            "pdis": "Adjustable aluminum laptop stand for better posture and cooling.",
            "pimage": "product/laptopstand.jpg",
            "c_id": 3
        },
        {
            "pname": "USB-C Hub",
            "pprice": 999,
            "pdis": "Multiport USB-C hub with HDMI, USB 3.0 and SD card reader.",
            "pimage": "product/usbhub.jpg",
            "c_id": 3
        },
        {
            "pname": "Power Bank 20000mAh",
            "pprice": 1599,
            "pdis": "Fast charging power bank with dual output and LED indicator.",
            "pimage": "product/powerbank.jpg",
            "c_id": 4
        },
        {
            "pname": "Mobile Charger 33W",
            "pprice": 499,
            "pdis": "33W fast charger adapter with USB Type-C cable support.",
            "pimage": "product/charger.jpg",
            "c_id": 4
        },
        {
            "pname": "LED Desk Lamp",
            "pprice": 899,
            "pdis": "Touch control LED lamp with brightness adjustment and eye protection.",
            "pimage": "product/desklamp.jpg",
            "c_id": 5
        }
    ]

    for item in products_seed_data:
        try:
            category = Category.objects.get(cid=item["c_id"])   # ✅ cid use karvu
        except Category.DoesNotExist:
            print(f"❌ Category cid {item['c_id']} not found, skipping: {item['pname']}")
            continue

        Product.objects.create(
            pname=item["pname"],
            pprice=item["pprice"],
            pdis=item["pdis"],
            pimage=item["pimage"],
            c_id=category
        )

    print("✅ 10 Products Seeded Successfully!")
