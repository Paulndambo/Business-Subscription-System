from decimal import Decimal

from django.test import TestCase

from products.models import Category, SubCategory, Product
from businesses.models import Business
from users.models import User


class CategoryModelsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")

    def test_category_can_be_created(self):
        self.assertEqual(str(self.category), "Food")
        self.assertEqual(self.category.name, "Food")
        self.assertIsInstance(self.category, Category)

    def test_category_name_must_be_string(self):
        self.assertIsInstance(self.category.name, str)


class SubCategoryModelsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")

        self.sub_category = SubCategory.objects.create(
            category=self.category, name="Vegetables"
        )

    def test_sub_category_can_be_created(self):
        self.assertEqual(self.sub_category.name, "Vegetables")
        self.assertIsInstance(self.sub_category, SubCategory)

    def test_sub_category_name_must_be_string(self):
        self.assertIsInstance(self.sub_category.name, str)

    def test_category_on_sub_category_is_a_member_of_category_class(self):
        self.assertIsInstance(self.sub_category.category, Category)


class ProductModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@gmail.com",
            phone_number="0745491093",
            gender="Male",
            role="Business Owner",
            password="John@123451234",
        )

        self.business = Business.objects.create(
            owner=self.user,
            name="Nairobi Wholesalers",
            location="Next to Machakos Country Bus",
            city="Nairobi",
            country="Kenya",
        )

        self.category = Category.objects.create(name="Food")

        self.sub_category = SubCategory.objects.create(
            category=self.category, name="Vegetables"
        )

        self.product = Product.objects.create(
            business=self.business,
            name="Spinanch",
            unit_price=Decimal(30),
            quantity=float(100),
            category=self.category,
            sub_category=self.sub_category,
        )

    def test_product_can_be_create(self):
        self.assertEqual(str(self.product), "Spinanch")

    def test_product_unit_price_is_decimal(self):
        self.assertIsInstance(self.product.unit_price, Decimal)

    def test_product_quantity_is_float(self):
        self.assertIsInstance(self.product.quantity, float)
