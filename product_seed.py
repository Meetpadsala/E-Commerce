from MyApp.models import Product, Category
from products_seed import products_seed_data

def run():
    for item in products_seed_data:
        category = Category.objects.get(id=item["c_id"])

        Product.objects.create(
            pname=item["pname"],
            pprice=item["pprice"],
            pdis=item["pdis"],
            pimage=item["pimage"],   # image path string
            c_id=category
        )

    print("10 Products Inserted Successfully!")
