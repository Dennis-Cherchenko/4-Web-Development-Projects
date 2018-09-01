# Project 3

In this project I used Django to create am updated version of the Pinocchio’s Pizza website.
I learned about jQuery and used it clean up the javascript and make things easier.

The site is layed out as have four main page: orders_manager, menu, shopping_cart, and orders
The orders_manager includes my personal touch and allows staff members to see all the orders in the database as well as modify the statuses.
The menu and shopping_cart implement the relevant functionalities.
The orders page lets the user see their order information and status (but not edit the status, thats is only available in the orders_manager)

The models.py is where I lay out all the different model objects for the site.

In the way of fancy restaurants, I made it so that the price for the items is only visible when it's in the cart, thus promoting a cleaner look.

I also made it so that the green and red don't extend all the way to the bottom all the time, in order to prevent the two colors from being overbearing.

A 'special' pizza supports up to 5 toppings.  Whether a user selects 4 or 5 toppings, they will charged for the 'special' pizza price.

Superuser:
username: JamesBond
password: qwertyqwerty
