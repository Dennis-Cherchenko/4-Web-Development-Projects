from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

# Import all the relevant models
from .models import Pizza, Pizza_Topping, Sub, Sub_Kind_Enum, Sub_Topping, Pasta, Salad, Dinner_Platter, \
                Dinner_Platter_Kind_Enum, Cart_Item, Order, Cart_Item_Pizza_Topping, Cart_Item_Sub_Topping

menu_objects = dict( pizzas=Pizza.objects.all(), pizza_toppings=Pizza_Topping.objects.all(),
                     subs=Sub.objects.all(), sub_kind_enum=Sub_Kind_Enum.objects.all(), sub_toppings=Sub_Topping.objects.all(),
                     pastas=Pasta.objects.all(), salads=Salad.objects.all(), dinner_platters=Dinner_Platter.objects.all(),
                     dinner_platter_kind_enum=Dinner_Platter_Kind_Enum.objects.all()
                    )


def menu(request):
    # Menu homepage
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})

    context = {
        "user": request.user,
        "menu_objects" : menu_objects,
        "cart_size" : getCartSize(request)
    }
    return render(request, "users/menu.html", context)


def login_view(request):

    # Login page

    username = request.POST.get("username")
    password = request.POST.get("password")

    if request.POST.get("isRegister") == "true":
        email = request.POST.get("email")
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})


def add_to_cart_view(request):

    # This is the function that is called when adding an item to the cart
    # It first checks the item_type and performs the relevant adding to the db as needed

    item_type = request.POST.get("item_type")
    if item_type == "pizza":
        kind = request.POST.get("kind")
        size = request.POST.get("size")
        pizza_topping_ids = request.POST.getlist("pizza_toppings")
        num_pizza_toppings = len(pizza_topping_ids)
        if num_pizza_toppings == 4:
            num_pizza_toppings = 5
        item_spec_id = Pizza.objects.all().filter(kind=kind, size=size, num_toppings=num_pizza_toppings)[0].id
        ci = Cart_Item.objects.create(
                                    user_id = request.user.id,
                                    item_type = item_type,
                                    item_spec_id = item_spec_id,
                                    order_id = 0
                                )

        for id in pizza_topping_ids:
            Cart_Item_Pizza_Topping(cart_item_id=ci.id, pizza_topping_id=id).save()

    elif item_type == "sub":
        kind = request.POST.get("kind")
        size = request.POST.get("size")
        sub_topping_ids = request.POST.getlist("sub_toppings")
        sub_id = Sub.objects.all().filter(kind=request.POST.get("kind"), size=request.POST.get("size"))[0].id
        ci = Cart_Item.objects.create(
                                    user_id = request.user.id,
                                    item_type = item_type,
                                    item_spec_id = sub_id,
                                    order_id = 0
                                )
        for id in sub_topping_ids:
            Cart_Item_Sub_Topping(cart_item_id=ci.id, sub_topping_id=id).save()

    elif item_type == "pasta":
        Cart_Item.objects.create(
                                    user_id = request.user.id,
                                    item_type = item_type,
                                    item_spec_id = request.POST.get("pasta_id"),
                                    order_id = 0
                                )
    elif item_type == "salad":
        Cart_Item.objects.create(
                                    user_id = request.user.id,
                                    item_type = item_type,
                                    item_spec_id = request.POST.get("salad_id"),
                                    order_id = 0
                                )
    elif item_type == "dinner_platter":
        item_spec_id = Dinner_Platter.objects.all().filter(kind=request.POST.get("kind"), size=request.POST.get("size"))[0].id
        Cart_Item.objects.create(
                                    user_id = request.user.id,
                                    item_type = item_type,
                                    item_spec_id = item_spec_id,
                                    order_id = 0
                                )

    return display_cart(request)

def cart_view(request):
    # Deletes an item in the cart
    cart_item_id = request.POST.get("delete_cart_item_id")
    if cart_item_id is not None:
        delete_Cart_Item(request, cart_item_id)

    return display_cart(request)


def delete_Cart_Item(request, cart_item_id):
    # Put the logic for delete the cart_item in a separate function
    if cart_item_id is not None:
        cart_item_object = getCartItemsForUser(request).filter(id=cart_item_id)[0]
        item_type = cart_item_object.item_type
        cart_item_id = cart_item_object.id

        if item_type == "pizza":
            for i in Cart_Item_Pizza_Topping.objects.all().filter(cart_item_id=cart_item_id):
                i.delete()
        elif item_type == "sub":
            for i in Cart_Item_Sub_Topping.objects.all().filter(cart_item_id=cart_item_id):
                i.delete()

        cart_item_object.delete()

class Cart_Item_Box():
    # The purpose of this 'box' is to allow for an object that can be sent to the html and js easily
    def __init__(self, ci_id, text):
        self.ci_id = ci_id
        self.text = text

def get_cart_item_text_and_config_cost(request, cart_item):

    # This is function to get what to print on the screen for a cart items

    if cart_item.item_type == "pizza":
        pizza = Pizza.objects.all().filter(id=cart_item.item_spec_id)[0]
        pizza_toppings = ""
        config_cost = pizza.cost
        for cipt in Cart_Item_Pizza_Topping.objects.all().filter(cart_item_id=cart_item.id):
            pizza_topping_object = Pizza_Topping.objects.all().filter(id=cipt.pizza_topping_id)[0]
            pizza_toppings += " " + pizza_topping_object.name
            config_cost += pizza_topping_object.cost

        return Cart_Item_Box(cart_item.id, pizza.kind + " pizza " + pizza.size + " $" + str(config_cost) \
                + " " + pizza_toppings), config_cost;

    elif cart_item.item_type == "sub":
        sub = Sub.objects.all().filter(id=cart_item.item_spec_id)[0]
        sub_toppings = ""
        config_cost = sub.cost
        for cipt in Cart_Item_Sub_Topping.objects.all().filter(cart_item_id=cart_item.id):
            sub_topping_object = Sub_Topping.objects.all().filter(id=cipt.sub_topping_id)[0]
            sub_toppings += " " + sub_topping_object.name
            config_cost += sub_topping_object.cost

        return Cart_Item_Box(cart_item.id, sub.kind + " sub " + sub.size \
                     + " $" + str(config_cost) + " " + sub_toppings), config_cost

    elif cart_item.item_type == "pasta":
        pasta = Pasta.objects.all().filter(id=cart_item.item_spec_id)[0]
        return Cart_Item_Box(cart_item.id, pasta.kind + " pasta $" + str(pasta.cost)), pasta.cost

    elif cart_item.item_type == "salad":
        salad = Salad.objects.all().filter(id=cart_item.item_spec_id)[0]
        return Cart_Item_Box(cart_item.id, salad.kind + " salad $" + str(salad.cost)), salad.cost

    elif cart_item.item_type == "dinner_platter":
        dinner_platter = Dinner_Platter.objects.all().filter(id=cart_item.item_spec_id)[0]
        return Cart_Item_Box(cart_item.id, dinner_platter.kind + " dinner platter " \
                            + dinner_platter.size + " $" + str(dinner_platter.cost)), dinner_platter.cost


def display_cart(request):

    # This function displays the cart page

    cart_items = []

    total = 0

    for cart_item in getCartItemsForUser(request).filter(user_id=request.user.id, order_id=0):
        item, config_cost =  get_cart_item_text_and_config_cost(request, cart_item)
        cart_items.append(item)
        total += config_cost


    context = {
        "user": request.user,
        "menu_objects" : menu_objects,
        "cart_items": cart_items,
        "cart_size" : getCartSize(request),
        "total": total
    }

    return render(request, "orders/cart.html", context)


def order_view(request):

    # This function returns the order view

    cart_item = request.POST.get("cart_item")

    if cart_item is not None:
        getCartItemsForUser(request).filter(id=request.POST.get("cart_item"))[0].delete()

    cart_items = Cart_Item.objects.all().exclude(order_id=0)

    context = {
        "user": request.user,
        "menu_objects" : menu_objects,
        "cart_items": cart_items,
        "cart_size" : getCartSize(request)
    }

    return render(request, "orders/order.html", context)

def confirmation_view(request):

    # This function returns the confirmation view

    cart_item_objects = getCartItemsForUser(request)

    timestamp = datetime.datetime.now()
    order = Order.objects.create(user_id=request.user.id, timestamp=datetime.datetime.now(), status = "Pending")

    for item in cart_item_objects:
        item.order_id = order.id
        item.save()


    cart_items = []
    total = 0

    for cart_item in cart_item_objects:
        item, config_cost =  get_cart_item_text_and_config_cost(request, cart_item)
        cart_items.append(item)
        total += config_cost

    context = {
        "user": request.user,
        "menu_objects" : menu_objects,
        "order_num" : order.id,
        "cart_size" : getCartSize(request),
        "cart_items": cart_items,
        "total" : total
    }

    return render(request, "orders/confirmation.html", context)

def orders_manager_view(request):

    # This function returns order_viewer that is only visible to staff members

    status = request.POST.get("status")
    order_id = request.POST.get("order_id")

    if status is not None:
        order = Order.objects.all().filter(id = order_id)[0]
        order.status = status
        order.save()

    order_item_boxes = []
    for order in Order.objects.all():
        cart_item_boxes = []
        for cart_item in Cart_Item.objects.all().filter(order_id=order.id):
            cart_item_boxes.append(get_cart_item_text_and_config_cost(request, cart_item)[0])
        username = User.objects.all().filter(id = order.user_id)[0].username
        order_item_boxes.append(Order_Item_Box(order.id, username, order.timestamp, order.status, cart_item_boxes))

    context = {
        "user": request.user,
        "menu_objects" : menu_objects,
        "order_item_boxes": order_item_boxes,
        "cart_size" : getCartSize(request)
    }

    return render(request, "orders/orders_manager.html", context)

def orders_view(request):

    # Lets user see their orders

    order_item_boxes = []
    for order in Order.objects.all().filter(user_id=request.user.id):
        cart_item_boxes = []
        for cart_item in Cart_Item.objects.all().filter(order_id=order.id):
            cart_item_boxes.append(get_cart_item_text_and_config_cost(request, cart_item)[0])
        username = User.objects.all().filter(id = order.user_id)[0].username
        order_item_boxes.append(Order_Item_Box(order.id, username, order.timestamp, order.status, cart_item_boxes))

    context = {
        "user": request.user,
        "menu_objects" : menu_objects,
        "order_item_boxes": order_item_boxes,
        "cart_size" : getCartSize(request),
    }

    return render(request, "orders/orders.html", context)

class Order_Item_Box():

    # The purpose of this 'box' is to allow for an object that can be sent to the html and js easily

    def __init__(self, order_id, username, timestamp, status, cart_item_boxes):
        self.order_id = order_id
        self.username = username
        self.timestamp = timestamp
        self.status = status
        self.cart_item_boxes = cart_item_boxes


# Below are two helper functions that help clean up the code by removing duplication

def getCartSize(request):
    return len(getCartItemsForUser(request))

def getCartItemsForUser(request, order_id = None):
    if order_id is None:
        return Cart_Item.objects.all().filter(user_id=request.user.id, order_id=0)
    else:
        return Cart_Item.objects.all().filter(user_id=request.user.id, order_id=order_id)


