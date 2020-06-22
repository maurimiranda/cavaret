from django.db import models
import django.utils.timezone

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False, db_index=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    tax_id = models.CharField(max_length=11, blank=True)
    discount = models.IntegerField(null=False, default=0)
    joined_at = models.DateField(default=django.utils.timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def discount_factor(self):
        return 1 - self.discount / 100

class Provider(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False, db_index=True)
    email = models.EmailField(blank=True)
    account_number = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total(self):
        total = Item.objects.filter(product__provider=self.id).aggregate(models.Sum('cost'))['cost__sum']
        if total == None:
            total = 0
        return round(total, 2)

    @property
    def paid(self):
        paid = self.payment_set.aggregate(models.Sum('amount'))['amount__sum']
        if paid == None:
            paid = 0
        return round(paid, 2)

    @property
    def balance(self):
        return round(self.total - self.paid, 2)

class Brand(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False, db_index=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, unique=True, blank=False, db_index=True)
    description = models.TextField(blank=True)
    cost = models.FloatField()
    price = models.FloatField()

    class Meta:
        ordering = ['brand', 'name']

    def __str__(self):
        return "%s - %s" % (self.brand, self.name)

    @property
    def profit(self):
        return round(self.price - self.cost, 2)

    @property
    def profit_percentage(self):
        if (self.price == 0):
            return 0
        return self.profit / self.price * 100

class Status(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True, blank=False, db_index=True)

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.name

class Order(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=django.utils.timezone.now)
    pickup_code = models.CharField(max_length=50, blank=True)
    tracking_code = models.CharField(max_length=50, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "#%s - %s" % (self.id, self.member)

    @property
    def total(self):
        return self.item_set.aggregate(models.Sum('price'))['price__sum']

    @property
    def quantity(self):
        return self.item_set.aggregate(models.Sum('quantity'))['quantity__sum']

class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=1)
    cost = models.FloatField(blank=True)
    price = models.FloatField(blank=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "%s - %s" % (self.order, self.product)

    def save(self, *args, **kwargs):
        if not self.cost:
            self.cost = self.product.cost * self.quantity
        if not self.price:
            self.price = (self.product.profit * self.order.member.discount_factor + self.product.cost) * self.quantity
        super().save(*args, **kwargs)

class Payment(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    date = models.DateTimeField(default=django.utils.timezone.now)
    amount = models.FloatField()
    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "%s - %s - $%s" % (self.id, self.date.date(), self.amount)
