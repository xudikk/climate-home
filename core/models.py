import datetime

from django.db import models

# Create your models here.
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=56)
    slug = models.SlugField(max_length=56, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.PositiveIntegerField()
    discount = models.SmallIntegerField(default=0, verbose_name="Chegirma Foizlarda")   # 15
    order_count = models.BigIntegerField(default=0)
    description = models.TextField()
    extra_desc = models.TextField(null=True, blank=True)

    ctg = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    date = models.DateTimeField(auto_now_add=True)

    def get_date(self, obj):
        hozir = datetime.datetime.now()
        minut = int((hozir - obj.date).total_seconds() // 60)
        if minut == 0:
            return "Hozir"
        if 0 < minut < 60:
            return f"{minut} minut oldin"
        return obj.date.strftime("%H:%M | %d/%m/%Y")

    def org_price(self):
        return f"{self.price:,}"

    def get_discount(self):
        return f"Skidka: {self.discount}%"

    def get_price(self):            # 1-0.15 => 0.85
        price = self.price * (1-(self.discount/100))
        return f"{int(price):,}"

    def get_image(self):
        return self.images.first().img


class ProductImg(models.Model):
    img = models.ImageField(upload_to="products/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")


class InfoProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='infos')
    key = models.CharField("Kalit", max_length=56)
    desc = models.CharField(max_length=256)



class Comment(models.Model):
    user = models.CharField(max_length=128)
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    img = models.ImageField(upload_to="blogs/", null=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField("Mavzu:", max_length=512)
    short_desc = models.TextField()
    link = models.URLField()


