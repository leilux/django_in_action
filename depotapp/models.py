from django.db import models

# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField()


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image_url = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # python manage.py dbshell
    # alter table depotapp_product add column date_available date not null default 0;
    # commit;
    date_available = models.DateField()
    orders = models.ManyToManyField(Order, through='LineItem')


class LineItem(models.Model):
    product = models.ForeignKey(Product, related_name='product')#, db_column='PROD')
    order = models.ForeignKey(Order)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
   

class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0

    def add_product(self, product):
        self.total_price += product.price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
                return
        self.items.append( LineItem(product=product, 
                                    unit_price=product.price,
                                    quantity=1))

