from django.db import models

class Pizza(models.Model):
      kind = models.CharField(max_length=32)
      num_toppings = models.IntegerField()
      size = models.CharField(max_length=1)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Pizza_Topping(models.Model):
      name = models.CharField(max_length=16)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Sub(models.Model):
      kind = models.CharField(max_length=32)
      size = models.CharField(max_length=1)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Sub_Kind_Enum(models.Model):
      kind = models.CharField(max_length=32)

class Sub_Topping(models.Model):
      name = models.CharField(max_length=16)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Pasta(models.Model):
      kind = models.CharField(max_length=32)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Salad(models.Model):
      kind = models.CharField(max_length=16)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Dinner_Platter(models.Model):
      kind = models.CharField(max_length=16)
      size = models.CharField(max_length=1)
      cost = models.DecimalField(max_digits=6, decimal_places=2)

class Dinner_Platter_Kind_Enum(models.Model):
      kind = models.CharField(max_length=32)

class Order(models.Model):
      user_id = models.CharField(max_length=64)
      timestamp = models.DateField()
      status = models.CharField(max_length=16)

class Cart_Item(models.Model):
      user_id = models.IntegerField()
      item_type = models.CharField(max_length=16)
      item_spec_id = models.IntegerField()
      order_id = models.IntegerField()

class Cart_Item_Pizza_Topping(models.Model):
      cart_item_id = models.IntegerField()
      pizza_topping_id = models.IntegerField()

class Cart_Item_Sub_Topping(models.Model):
      cart_item_id = models.IntegerField()
      sub_topping_id = models.IntegerField()
