import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Slider
from products.models import Category, Brand, Product
from orders.models import Order, OrderItem

User = get_user_model()


class Command(BaseCommand):
    help = 'ساخت داده‌ی نمونه برای تمام مدل‌های پروژه (تست گزارش‌ها و دمو)'

    def handle(self, *args, **kwargs):
        self.stdout.write('شروع ساخت داده‌ی نمونه...')

        # ۱. دسته‌بندی‌ها
        category_names = ['ابزار برقی', 'ابزار دستی', 'لوازم جانبی', 'تجهیزات ایمنی']
        categories = []
        for name in category_names:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={'slug': name.replace(' ', '-')}
            )
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f'{len(categories)} دسته‌بندی آماده شد'))

        # ۲. برندها
        brand_names = ['بوش', 'ماکیتا', 'دیوالت', 'اینگرسال']
        brands = []
        for name in brand_names:
            brand, _ = Brand.objects.get_or_create(name=name)
            brands.append(brand)
        self.stdout.write(self.style.SUCCESS(f'{len(brands)} برند آماده شد'))

        # ۳. محصولات
        product_names = [
            'دریل برقی', 'پیچ‌گوشتی شارژی', 'اره‌مویی', 'فرز آهنگری',
            'چکش برقی', 'دستکش ایمنی', 'عینک محافظ', 'متر لیزری',
            'جعبه ابزار', 'کمپرسور هوا'
        ]
        products = []
        for name in product_names:
            product, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': random.choice(categories),
                    'brand': random.choice(brands),
                    'price': Decimal(random.randrange(50000, 3000000, 10000)),
                    'stock': random.randint(0, 50),
                    'description': f'توضیحات نمونه برای {name}',
                }
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f'{len(products)} محصول آماده شد'))

        # ۴. اسلایدرها
        slider_titles = ['حراج تابستانه', 'محصولات جدید', 'تخفیف ویژه اعضا']
        for i, title in enumerate(slider_titles):
            Slider.objects.get_or_create(
                title=title,
                defaults={'link': '/products/', 'order': i}
            )
        self.stdout.write(self.style.SUCCESS(f'{len(slider_titles)} اسلاید آماده شد'))
        self.stdout.write(self.style.WARNING('توجه: تصاویر اسلایدر باید دستی از پنل ادمین آپلود بشن'))

        # ۵. کاربران (مشتری، فروشنده)
        customers = []
        for i in range(10):
            user, created = User.objects.get_or_create(
                username=f'customer{i}',
                defaults={
                    'email': f'customer{i}@test.com',
                    'role': 'customer',
                }
            )
            if created:
                user.set_password('test12345')
                user.save()
            customers.append(user)

        for i in range(2):
            user, created = User.objects.get_or_create(
                username=f'staff{i}',
                defaults={
                    'email': f'staff{i}@test.com',
                    'role': 'staff',
                }
            )
            if created:
                user.set_password('test12345')
                user.save()

        self.stdout.write(self.style.SUCCESS(f'{len(customers)} مشتری و ۲ فروشنده آماده شد'))

        # ۶. سفارش‌ها و آیتم‌های سفارش
        status_options = ['pending', 'processing', 'shipped', 'completed']
        order_count = 0
        for customer in customers:
            num_orders = random.randint(1, 5)
            for _ in range(num_orders):
                status = random.choice(status_options)
                order = Order.objects.create(
                    user=customer,
                    status=status,
                    is_paid=(status != 'pending'),
                )

                selected_products = random.sample(products, k=random.randint(1, 4))
                total = Decimal('0')
                for product in selected_products:
                    quantity = random.randint(1, 3)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )
                    total += product.price * quantity

                order.total_price = total
                order.save()
                order_count += 1

        self.stdout.write(self.style.SUCCESS(f'{order_count} سفارش با آیتم‌هاشون ساخته شد'))

        self.stdout.write(self.style.SUCCESS('✅ داده‌ی نمونه با موفقیت کامل ساخته شد!'))