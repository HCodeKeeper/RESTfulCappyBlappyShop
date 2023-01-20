from django.db import models
from django.contrib.auth import get_user_model
DOESNT_EXIST_ID = -1


class Telephone(models.Model):
    number = models.CharField(max_length=15, unique=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    image_src = models.CharField(max_length=256)
    rating = models.SmallIntegerField(default=0)
    description = models.CharField(max_length=5000)
    manufacturer = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    # ALWAYS USD
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Deal(models.Model):
    title = models.CharField(max_length=50)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    percents = models.FloatField(max_length=3)

    def __str__(self):
        return f"{self.title} ({self.percents}%)"


class Addon(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} for {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    rating = models.SmallIntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    text = models.CharField(max_length=1000, default="")

    def __str__(self):
        return f"for {self.product.name}"


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, null=True)
    creation_date = models.DateTimeField()
    email = models.EmailField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"order for ${self.price} $"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    addon = models.ForeignKey(Addon, null=True, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        addon_name = "+ " + self.addon.name if self.addon else ''
        return f"{self.product.name} {addon_name} x{self.quantity} Order#{self.order.id}"
