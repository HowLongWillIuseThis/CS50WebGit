from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return self.category

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts", null=True, blank=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    image_url = models.URLField(max_length=2000)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    price = models.DecimalField(decimal_places=2, max_digits=9)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Comment(models.Model):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders", null=True, blank=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="items", default=None)
    bid = models.DecimalField(decimal_places=2, max_digits=9, default=0)