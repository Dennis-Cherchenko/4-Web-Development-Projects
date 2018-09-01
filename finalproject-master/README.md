# Final Project

For technologies I used HTML, CSS, Django, SQLite database, Python.
My project lives on the C9 IDE environment.


For my final project I made an exclusive members-only portfolio website where users can upload their
posts of photography and works of writing.

I split up the website into different pages:
On entering the website the user is asked to login/register.  Then they land on the homepage which is the newsfeed.
There, they can see the most-liked posts based on a filter and browse all the latest uploaded posts.
Then the user can click on a selected post and open the post in a full post view, which has all the likes and comments
and information too.  The user can also open up the porfolio page which is a nice view of all the posts of all the posts
and user has made.  There is also the search functionality where results are returned matching both users and posts.

I would like to thank Vitor Freitas for his very useful Django tutorial on how to upload files.
https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
https://github.com/sibtc/simple-file-upload

In addition to views.py, I also have a file manager.py where I outsourced a lot of 'lower-level' functions so that
they could all be in one place and wouldn't clutter up views.py

For sample post purposes I used public domain images from https://www.pexels.com/public-domain-images/

The superuser account is:
username: JamesBond
password: qazwsxedc

Other accounts to try are:
usernames: ElonMusk, TimCook, BillGaes, JeffBezos
passowrd: qazwsxedc


