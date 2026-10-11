from products.models import Product

class Cart:
    def __init__(self, request):          # add previous cart
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

 
    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
          self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        current_quantity = self.cart[product_id]['quantity']

        if current_quantity + quantity > product.stock:
          return False  # موجودی کافی نیست

        self.cart[product_id]['quantity'] += quantity
        self.save()
        return True


    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()


    def get_quantity(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
        return 0


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def save(self):
        self.session.modified = True


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            yield {
                'product': product,
                'quantity': item['quantity'],
                'price': float(item['price']),
                'total_price': float(item['price']) * item['quantity'],
            }

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()