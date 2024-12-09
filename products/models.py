from django.db import models

from core.models import AbstractBaseModel


# Create your models here.
class Category(AbstractBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubCategory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product(AbstractBaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    business = models.ForeignKey(
        "businesses.Business", on_delete=models.CASCADE, related_name="products"
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.FloatField(default=0)
    image = models.ImageField(upload_to="products_images/", null=True)

    def __str__(self):
        return self.name


class ProductImage(AbstractBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products_images/", null=True)

    def __str__(self):
        return self.product.name
