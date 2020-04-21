from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    availability = models.BooleanField()
    price = models.PositiveIntegerField()
    item_picture = models.CharField(max_length=1500)

    def __str__(self):
        return self.name

