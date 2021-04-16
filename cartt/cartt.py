from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cartt(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cartt = self.session.get(settings.CARTT_SESSION_ID)
        if not cartt:
            # save an empty cart in the session
            cartt = self.session[settings.CARTT_SESSION_ID] = {}
        self.cartt = cartt

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cartt.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cartt = self.cartt.copy()
        for product in products:
            cartt[str(product.id)]['product'] = product

        for item in cartt.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cartt.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cartt:
            self.cartt[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if override_quantity:
            self.cartt[product_id]['quantity'] = quantity
        else:
            self.cartt[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cartt:
            del self.cartt[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CARTT_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cartt.values())